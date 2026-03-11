from __future__ import annotations

from mcp.types import TextContent, Tool

from crypto_mcp.clients.coingecko import CoinGeckoClient

tool_definition = Tool(
    name="get_market",
    description=(
        "Get the top N cryptocurrencies on CoinGecko in the last 24 hours. "
        "Returns coin ID, name, symbol, market cap rank, and 24h price change for each."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "currency": {"type": "string", "description": "Currency code e.g. 'usd', 'eur'", "default": "usd"},
            "top_n": {"type": "integer", "description": "Number of top coins to return", "default": 10},
        },
        "required": ["currency", "top_n"],
    },
)


async def run(arguments: dict) -> list[TextContent]:
    currency = arguments.get("currency", "usd")
    top_n = arguments.get("top_n", 10)
    async with CoinGeckoClient() as client:
        markets = await client.get_market(currency, top_n)
    return [TextContent(type="text", text=market.to_text()) for market in markets]
