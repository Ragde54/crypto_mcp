from unittest.mock import AsyncMock, patch

import pytest

from crypto_mcp.server import call_tool, get_prompt, list_prompts, list_tools


async def test_list_tools_returns_all():
    result = await list_tools()
    assert len(result) == 3
    tool_names = [tool.name for tool in result]
    assert "get_price" in tool_names
    assert "get_trending" in tool_names
    assert "get_market" in tool_names


async def test_call_price_tool(mock_coingecko_client, sample_coin_price):
    with patch(
        "crypto_mcp.tools.price.CoinGeckoClient",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_coingecko_client), __aexit__=AsyncMock(return_value=False)
        ),
    ):
        result = await call_tool("get_price", {"coin_id": "bitcoin", "currency": "usd"})

    assert len(result) == 1
    assert "bitcoin" in result[0].text.lower()


async def test_call_unknown_tool():
    with pytest.raises(ValueError, match="not found"):
        await call_tool("nonexistent_tool", {})


async def test_list_prompts():
    result = await list_prompts()
    assert len(result) == 1
    assert result[0].name == "analyze-crypto"


async def test_get_prompt(sample_coin_price):
    result = await get_prompt("analyze-crypto", {"coin_id": "bitcoin", "data": sample_coin_price.to_text()})
    assert len(result.messages) == 1
    assert "bitcoin" in result.messages[0].content.text.lower()


async def test_get_unknown_prompt():
    with pytest.raises(ValueError, match="not found"):
        await get_prompt("nonexistent_prompt", {})
