import pytest

from crypto_mcp.models.crypto import CoinMarket, CoinPrice, TrendingCoin


# --- Test CoinPrice ---

def test_coin_price_happy_path(sample_price_response):
    price = CoinPrice.from_api_response(
        data=sample_price_response,
        coin_id="bitcoin",
        currency="usd"
    )
    assert price.coin_id == "bitcoin"
    assert price.currency == "usd"
    assert price.price == 66060.0
    assert price.change_24h == -1.79


def test_coin_price_missing_change(sample_price_response):
    sample_price_response["bitcoin"].pop("usd_24h_change")
    price = CoinPrice.from_api_response(
        data=sample_price_response,
        coin_id="bitcoin",
        currency="usd"
    )
    assert price.change_24h is None


def test_coin_price_different_currency():
    data = {"ethereum": {"eur": 3000.0, "eur_24h_change": 1.5}}
    price = CoinPrice.from_api_response(
        data=data,
        coin_id="ethereum",
        currency="eur"
    )
    assert price.price == 3000.0
    assert price.change_24h == 1.5


def test_coin_price_invalid_coin(sample_price_response):
    with pytest.raises(KeyError):
        CoinPrice.from_api_response(
            data=sample_price_response,
            coin_id="notacoin",
            currency="usd"
        )


# --- Test TrendingCoin ---

def test_trending_coin_happy_path(sample_trending_response):
    coin = TrendingCoin.from_api_response(sample_trending_response["coins"][0])
    assert coin.coin_id == "bitcoin"
    assert coin.name == "Bitcoin"
    assert coin.symbol == "BTC"
    assert coin.market_cap_rank == 1
    assert coin.change_24h == 0.58
    
def test_trending_missing_data(sample_trending_response):
    sample_trending_response["coins"][0]["item"].pop("data")
    coin = TrendingCoin.from_api_response(sample_trending_response["coins"][0])
    assert coin.change_24h is None
    
def test_trending_to_text(sample_trending_response):
    coin = TrendingCoin.from_api_response(sample_trending_response["coins"][0])
    assert coin.to_text() == "Bitcoin (BTC) | Rank: 1 | 24h change: 0.58%"

def test_trending_to_text_missing_data(sample_trending_response):
    sample_trending_response["coins"][0]["item"].pop("data")
    coin = TrendingCoin.from_api_response(sample_trending_response["coins"][0])
    assert coin.to_text() == "Bitcoin (BTC) | Rank: 1 | 24h change: N/A"
    

# --- Test CoinMarket ---

def test_coin_market_happy_path(sample_market_response):
    coin = CoinMarket.from_api_response(sample_market_response[0])
    assert coin.coin_id == "bitcoin"
    assert coin.name == "Bitcoin"
    assert coin.symbol == "BTC"
    assert coin.current_price == 67883.0
    assert coin.market_cap == 1358579644402
    assert coin.change_24h == 712.43

def test_coin_market_missing_data(sample_market_response):
    sample_market_response[0].pop("market_cap")
    coin = CoinMarket.from_api_response(sample_market_response[0])
    assert coin.market_cap is None
    
def test_coin_market_to_text(sample_market_response):
    coin = CoinMarket.from_api_response(sample_market_response[0])
    assert coin.to_text() == "Bitcoin (BTC) | Current price: 67883.0 | Market cap: 1,358,579,644,402 | 24h change: 712.43"

def test_coin_market_to_text_missing_data(sample_market_response):
    sample_market_response[0].pop("market_cap")
    coin = CoinMarket.from_api_response(sample_market_response[0])
    assert coin.to_text() == "Bitcoin (BTC) | Current price: 67883.0 | Market cap: N/A | 24h change: 712.43"