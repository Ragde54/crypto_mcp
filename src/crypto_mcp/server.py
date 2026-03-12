import asyncio
import logging
import time
from typing import Any

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import GetPromptResult, Prompt, Resource, TextContent, Tool
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from pydantic import AnyUrl

from crypto_mcp import __version__
from crypto_mcp.logging import setup_logging
from crypto_mcp.prompts.analysis import get_prompt as analysis_get_prompt
from crypto_mcp.prompts.analysis import prompt as analysis_prompt
from crypto_mcp.tools.markets import run as market_run
from crypto_mcp.tools.markets import tool_definition as market_definition
from crypto_mcp.tools.price import run as price_run
from crypto_mcp.tools.price import tool_definition as price_definition
from crypto_mcp.tools.trending import run as trending_run
from crypto_mcp.tools.trending import tool_definition as trending_definition

# Instantiate server
app = Server("crypto-mcp")

tool_definitions = [price_definition, trending_definition, market_definition]
prompt_definitions = [analysis_prompt]

tool_runners = {
    "get_price": price_run,
    "get_trending": trending_run,
    "get_market": market_run,
}

prompt_runners = {
    "analyze-crypto": analysis_get_prompt,
}

# Setup OpenTelemetry (no exporters configured by default to avoid stdout corruption)
provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

logger = logging.getLogger(__name__)


# Resources handler
@app.list_resources()  # type: ignore[no-untyped-call,untyped-decorator]
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri=AnyUrl("info://crypto-mcp/version"),
            name="Server Information",
            mimeType="application/json",
            description="Returns version and general server info",
        )
    ]


@app.read_resource()  # type: ignore[no-untyped-call,untyped-decorator]
async def read_resource(uri: str) -> str:
    if str(uri) == "info://crypto-mcp/version":
        return f'{{\n  "name": "crypto-mcp",\n  "version": "{__version__}"\n}}'
    raise ValueError(f"Resource not found: {uri}")


# List tools handler
@app.list_tools()  # type: ignore[no-untyped-call,untyped-decorator]
async def list_tools() -> list[Tool]:
    return tool_definitions


@app.call_tool()  # type: ignore[untyped-decorator]
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name not in tool_runners:
        raise ValueError(f"Tool not found: {name}")

    coin_id = arguments.get("coin_id")
    start_time = time.perf_counter()

    with tracer.start_as_current_span(f"tool_call:{name}") as span:
        span.set_attribute("tool_name", name)
        if coin_id:
            span.set_attribute("coin_id", coin_id)

        try:
            result = await tool_runners[name](arguments)
            latency_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Tool call successful",
                extra={
                    "tool_name": name,
                    "coin_id": coin_id,
                    "latency_ms": round(latency_ms, 2),
                    "success": True,
                },
            )
            span.set_attribute("success", True)
            return result
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                "Tool call failed",
                exc_info=True,
                extra={
                    "tool_name": name,
                    "coin_id": coin_id,
                    "latency_ms": round(latency_ms, 2),
                    "success": False,
                    "error": str(e),
                },
            )
            span.set_attribute("success", False)
            span.record_exception(e)
            raise


@app.list_prompts()  # type: ignore[no-untyped-call,untyped-decorator]
async def list_prompts() -> list[Prompt]:
    return prompt_definitions


@app.get_prompt()  # type: ignore[no-untyped-call,untyped-decorator]
async def get_prompt(name: str, arguments: dict[str, Any]) -> GetPromptResult:
    if name not in prompt_runners:
        raise ValueError(f"Prompt not found: {name}")
    return prompt_runners[name](**arguments)


async def main() -> None:
    setup_logging()
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="crypto-mcp",
                server_version=__version__,
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
