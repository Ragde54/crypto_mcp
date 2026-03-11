import asyncio
from typing import Any

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import GetPromptResult, Prompt, TextContent, Tool

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


# List tools handler
@app.list_tools()  # type: ignore[no-untyped-call,untyped-decorator]
async def list_tools() -> list[Tool]:
    return tool_definitions


@app.call_tool()  # type: ignore[untyped-decorator]
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name not in tool_runners:
        raise ValueError(f"Tool not found: {name}")
    return await tool_runners[name](arguments)


@app.list_prompts()  # type: ignore[no-untyped-call,untyped-decorator]
async def list_prompts() -> list[Prompt]:
    return prompt_definitions


@app.get_prompt()  # type: ignore[no-untyped-call,untyped-decorator]
async def get_prompt(name: str, arguments: dict[str, Any]) -> GetPromptResult:
    if name not in prompt_runners:
        raise ValueError(f"Prompt not found: {name}")
    return prompt_runners[name](**arguments)


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="crypto-mcp",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
