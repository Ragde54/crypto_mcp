from mcp.types import GetPromptResult, Prompt, PromptArgument, PromptMessage, TextContent

prompt = Prompt(
    name="analyze-crypto",
    description="Analyze cryptocurrency data and provide a structured market analysis.",
    arguments=[
        PromptArgument(name="coin_id", description="CoinGecko coin ID e.g. 'bitcoin', 'ethereum'", required=True),
        PromptArgument(name="data", description="Price data to analyze", required=True),
    ],
)


def get_prompt(coin_id: str, data: str) -> GetPromptResult:
    return GetPromptResult(
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=(
                        f"You are a cryptocurrency market analyst.\n\n"
                        f"Analyze the following data for {coin_id}:\n{data}\n\n"
                        "Provide a structured analysis covering:\n"
                        "1. Current price assessment\n"
                        "2. 24h trend interpretation (Bullish / Bearish / Neutral)\n"
                        "3. Brief reasoning based on the numbers\n\n"
                        "Important: state clearly this is NOT financial advice."
                    ),
                ),
            )
        ]
    )
