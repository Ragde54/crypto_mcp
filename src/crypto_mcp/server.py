import asyncio

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from crypto_mcp.clients.coingecko import CoinGeckoClient
from crypto_mcp.config import settings

# Instantiate server
app = Server("crypto-mcp")

# List tools handler
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_price",
            description=(
                "Get the current price of a cryptocurrency "
                "by its CoinGecko ID (e.g. 'bitcoin', 'ethereum'). "
                "Returns price and 24h change."
            ),
            inputSchema={
                "type": "object",
                "properties":{
                    "coin_id":{"type":"string"},
                    "currency":{"type":"string", "default": "usd"},
                },
                "required":["coin_id"]
            })
    ]

@app.call_tool()
async def tool_call(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "get_price":
            coin_id = arguments.get("coin_id")
            if not coin_id:
                raise ValueError("coin_id is required")
            currency = arguments.get("currency", "usd")
            async with CoinGeckoClient() as client:
                price = await client.get_price(coin_id, currency)
                change = f"{round(price.change_24h, 2)}%" if price.change_24h is not None else "N/A"
                answer = f"{coin_id.capitalize()} is {price.price} {currency.upper()}\n24h change: {change}"
        return [TextContent(type="text", text=answer)]
    except Exception as e:
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]
    
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream,
                    write_stream, 
                    InitializationOptions(
                        server_name="crypto-mcp",
                        server_version="0.1.0",
                        capabilities=app.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={},
                        ),
                    ))
        
if __name__ == "__main__":
    asyncio.run(main())