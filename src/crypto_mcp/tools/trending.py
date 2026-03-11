from __future__ import annotations

from typing import Any

from mcp.types import TextContent, Tool

from crypto_mcp.clients.coingecko import CoinGeckoClient

tool_definition = Tool(
    name="get_trending",
    description=(
        "Get the top 7 trending cryptocurrencies on CoinGecko in the last 24 hours. "
        "Returns coin ID, name, symbol, market cap rank, and 24h price change for each."
    ),
    inputSchema={"type": "object", "properties": {}, "required": []},
)


async def run(arguments: dict[str, Any]) -> list[TextContent]:
    async with CoinGeckoClient() as client:
        trending = await client.get_trending()
    return [TextContent(type="text", text=coin.to_text()) for coin in trending]
