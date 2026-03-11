from __future__ import annotations

from typing import Any

from mcp.types import TextContent, Tool

from crypto_mcp.clients.coingecko import CoinGeckoClient

tool_definition = Tool(
    name="get_price",
    description=(
        "Get the current price of a cryptocurrency "
        "by its CoinGecko ID (e.g. 'bitcoin', 'ethereum'). "
        "Returns price and 24h change."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "coin_id": {"type": "string", "description": "CoinGecko coin ID e.g. 'bitcoin', 'ethereum'"},
            "currency": {"type": "string", "description": "Currency code e.g. 'usd', 'eur'", "default": "usd"},
        },
        "required": ["coin_id"],
    },
)


async def run(arguments: dict[str, Any]) -> list[TextContent]:
    coin_id = arguments.get("coin_id")
    if not coin_id:
        raise ValueError("coin_id is required")
    currency = arguments.get("currency", "usd")
    async with CoinGeckoClient() as client:
        price = await client.get_price(coin_id, currency)
    return [TextContent(type="text", text=price.to_text())]
