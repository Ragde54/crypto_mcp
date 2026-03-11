import httpx
import pytest
import respx

from crypto_mcp.clients.coingecko import CoinGeckoClient

# --- Test get_price ---


@respx.mock
async def test_get_price_success(sample_price_response):
    respx.get("https://api.coingecko.com/api/v3/simple/price").mock(
        return_value=httpx.Response(200, json=sample_price_response)
    )
    async with CoinGeckoClient() as client:
        result = await client.get_price("bitcoin", "usd")
    assert result.coin_id == "bitcoin"
    assert result.price == 66060.0
    assert result.change_24h == -1.79


@respx.mock
async def test_get_price_not_found():
    respx.get("https://api.coingecko.com/api/v3/simple/price").mock(return_value=httpx.Response(404, json={}))
    with pytest.raises(ValueError, match="not found"):
        async with CoinGeckoClient() as client:
            await client.get_price("bitcoin", "usd")


@respx.mock
async def test_get_price_rate_limit():
    respx.get("https://api.coingecko.com/api/v3/simple/price").mock(return_value=httpx.Response(429, json={}))
    with pytest.raises(ValueError, match="Rate limit exceeded"):
        async with CoinGeckoClient() as client:
            await client.get_price("bitcoin", "usd")


@respx.mock
async def test_get_price_unexpected_error():
    respx.get("https://api.coingecko.com/api/v3/simple/price").mock(return_value=httpx.Response(500, json={}))
    with pytest.raises(httpx.HTTPStatusError):
        async with CoinGeckoClient() as client:
            await client.get_price("bitcoin", "usd")


@respx.mock
async def test_get_price_no_change_24h(sample_price_response):
    sample_price_response["bitcoin"]["usd_24h_change"] = None
    respx.get("https://api.coingecko.com/api/v3/simple/price").mock(
        return_value=httpx.Response(200, json=sample_price_response)
    )
    async with CoinGeckoClient() as client:
        result = await client.get_price("bitcoin", "usd")
    assert result.change_24h is None


# --- Test get_trending ---


@respx.mock
async def test_get_trending_happy_path(sample_trending_response):
    respx.get("https://api.coingecko.com/api/v3/search/trending").mock(
        return_value=httpx.Response(200, json=sample_trending_response)
    )
    async with CoinGeckoClient() as client:
        result = await client.get_trending()
    coin = result[0]
    assert len(result) > 0
    assert coin.coin_id == "bitcoin"
    assert coin.name == "Bitcoin"
    assert coin.symbol == "BTC"
    assert coin.market_cap_rank == 1
    assert coin.change_24h == 0.58


@respx.mock
async def test_get_trending_limit(sample_trending_response):
    respx.get("https://api.coingecko.com/api/v3/search/trending").mock(
        return_value=httpx.Response(200, json=sample_trending_response)
    )
    async with CoinGeckoClient() as client:
        result = await client.get_trending()
    assert len(result) <= 7

@respx.mock
async def test_get_trending_not_found():
    respx.get("https://api.coingecko.com/api/v3/search/trending").mock(return_value=httpx.Response(404, json={}))
    with pytest.raises(ValueError, match="not found"):
        async with CoinGeckoClient() as client:
            await client.get_trending()


@respx.mock
async def test_get_trending_rate_limit():
    respx.get("https://api.coingecko.com/api/v3/search/trending").mock(return_value=httpx.Response(429, json={}))
    with pytest.raises(ValueError, match="Rate limit exceeded"):
        async with CoinGeckoClient() as client:
            await client.get_trending()


@respx.mock
async def test_get_trending_unexpected_error():
    respx.get("https://api.coingecko.com/api/v3/search/trending").mock(return_value=httpx.Response(500, json={}))
    with pytest.raises(httpx.HTTPStatusError):
        async with CoinGeckoClient() as client:
            await client.get_trending()


# --- Test get_market ---


@respx.mock
async def test_get_market_happy_path(sample_market_response):
    respx.get("https://api.coingecko.com/api/v3/coins/markets").mock(
        return_value=httpx.Response(200, json=sample_market_response)
    )
    async with CoinGeckoClient() as client:
        result = await client.get_market("usd", 10)
    coin = result[0]
    assert len(result) > 0
    assert coin.coin_id == "bitcoin"
    assert coin.name == "Bitcoin"
    assert coin.symbol == "BTC"
    assert coin.current_price == 67883.0
    assert coin.market_cap == 1358579644402
    assert coin.change_24h == 712.43


@respx.mock
async def test_get_market_top_n(sample_market_response):
    route = respx.get("https://api.coingecko.com/api/v3/coins/markets").mock(
        return_value=httpx.Response(200, json=sample_market_response)
    )
    async with CoinGeckoClient() as client:
        await client.get_market(currency="usd", top_n=5)

    assert route.called
    request = route.calls.last.request
    assert "per_page=5" in str(request.url)


@respx.mock
async def test_get_market_not_found():
    respx.get("https://api.coingecko.com/api/v3/coins/markets").mock(return_value=httpx.Response(404, json={}))
    with pytest.raises(ValueError, match="not found"):
        async with CoinGeckoClient() as client:
            await client.get_market("usd", 10)


@respx.mock
async def test_get_market_rate_limit():
    respx.get("https://api.coingecko.com/api/v3/coins/markets").mock(return_value=httpx.Response(429, json={}))
    with pytest.raises(ValueError, match="Rate limit exceeded"):
        async with CoinGeckoClient() as client:
            await client.get_market("usd", 10)


@respx.mock
async def test_get_market_unexpected_error():
    respx.get("https://api.coingecko.com/api/v3/coins/markets").mock(return_value=httpx.Response(500, json={}))
    with pytest.raises(httpx.HTTPStatusError):
        async with CoinGeckoClient() as client:
            await client.get_market("usd", 10)