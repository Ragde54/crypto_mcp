from unittest.mock import AsyncMock, patch

import pytest

from crypto_mcp.tools.markets import run as market_run
from crypto_mcp.tools.price import run as price_run
from crypto_mcp.tools.trending import run as trending_run

# --- Test get_price ---


async def test_get_price_success(mock_coingecko_client, sample_coin_price):
    with patch(
        "crypto_mcp.tools.price.CoinGeckoClient",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_coingecko_client), __aexit__=AsyncMock(return_value=False)
        ),
    ):
        result = await price_run({"coin_id": "bitcoin", "currency": "usd"})

    assert len(result) == 1
    assert "bitcoin" in result[0].text.lower()
    assert "66060" in result[0].text


async def test_get_price_missing_coin_id():
    with pytest.raises(ValueError, match="required"):
        await price_run({})


async def test_get_price_empty_coin_id():
    with pytest.raises(ValueError, match="required"):
        await price_run({"coin_id": ""})


async def test_get_price_none_change_24h(mock_coingecko_client, sample_coin_price):
    sample_coin_price.change_24h = None
    with patch(
        "crypto_mcp.tools.price.CoinGeckoClient",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_coingecko_client), __aexit__=AsyncMock(return_value=False)
        ),
    ):
        result = await price_run({"coin_id": "bitcoin", "currency": "usd"})

    assert "N/A" in result[0].text


# --- Test get_trending ---


async def test_get_trending_success(mock_coingecko_client, sample_trending_coins):
    with patch(
        "crypto_mcp.tools.trending.CoinGeckoClient",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_coingecko_client), __aexit__=AsyncMock(return_value=False)
        ),
    ):
        result = await trending_run({})

    assert len(result) == 7
    assert "bitcoin" in result[0].text.lower()
    assert "bittensor" in result[1].text.lower()
    assert "pi network" in result[2].text.lower()
    assert "pudgy penguins" in result[3].text.lower()
    assert "neiro" in result[4].text.lower()
    assert "solana" in result[5].text.lower()
    assert "ethereum" in result[6].text.lower()


# --- Test get_markets ---


async def test_get_markets_success(mock_coingecko_client, sample_coin_markets):
    with patch(
        "crypto_mcp.tools.markets.CoinGeckoClient",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_coingecko_client), __aexit__=AsyncMock(return_value=False)
        ),
    ):
        result = await market_run({"currency": "usd", "top_n": 3})

    assert len(result) == 3
    assert "bitcoin" in result[0].text.lower()
    assert "ethereum" in result[1].text.lower()
    assert "solana" in result[2].text.lower()


async def test_get_market_missing_data(mock_coingecko_client, sample_coin_markets):
    sample_coin_markets[0].market_cap = None
    with patch(
        "crypto_mcp.tools.markets.CoinGeckoClient",
        return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_coingecko_client), __aexit__=AsyncMock(return_value=False)
        ),
    ):
        result = await market_run({"currency": "usd", "top_n": 3})
    assert "N/A" in result[0].text
