import asyncio
from mcp.server import Server, NotificationOptions
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions

# Instantiate server
app = Server("crypto-mcp")

# List tools handler
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_price",
            description="Get the current price of a cryptocurrency by its CoinGecko ID (e.g. 'bitcoin', 'ethereum'). Returns price and 24h change.",
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
    if name == "get_price":
        coin_id = arguments.get("coin_id")
        if not coin_id:
            raise ValueError("coin_id is required")
        currency = arguments.get("currency", "usd")
        #return [TextContent(text=f"Price of {coin_id} in {currency}: $100")]
        return [TextContent(type="text",
                            text="Bitcoin (BTC): $50,000 | 24h change: +2.5%")]
    raise ValueError(f"Tool not found: {name}")
    
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