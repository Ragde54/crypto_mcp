from unittest.mock import AsyncMock

import pytest

from crypto_mcp.clients.coingecko import CoinGeckoClient
from crypto_mcp.models.crypto import CoinMarket, CoinPrice, TrendingCoin

# ---------------------------------------------------------------------------
# Raw API response fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_price_response():
    return {"bitcoin": {"usd": 66060.0, "usd_24h_change": -1.79}}


@pytest.fixture
def sample_trending_response():
    return {
        "coins": [
            {
                "item": {
                    "id": "bitcoin",
                    "coin_id": 0,
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "market_cap_rank": 1,
                    "thumb": "",
                    "small": "",
                    "large": "",
                    "slug": "",
                    "price_btc": 0,
                    "score": 0,
                    "data": {
                        "price": 0,
                        "price_btc": "",
                        "price_change_percentage_24h": {"usd": 0.58},
                        "market_cap": "",
                        "market_cap_btc": "",
                        "total_volume": "",
                        "total_volume_btc": "",
                        "sparkline": "",
                        "content": {"title": "", "description": ""},
                    },
                }
            },
            {
                "item": {
                    "id": "bittensor",
                    "coin_id": 0,
                    "name": "Bittensor",
                    "symbol": "TAO",
                    "market_cap_rank": 45,
                    "thumb": "",
                    "small": "",
                    "large": "",
                    "slug": "",
                    "price_btc": 0,
                    "score": 0,
                    "data": {
                        "price": 0,
                        "price_btc": "",
                        "price_change_percentage_24h": {"usd": 0.3},
                        "market_cap": "",
                        "market_cap_btc": "",
                        "total_volume": "",
                        "total_volume_btc": "",
                        "sparkline": "",
                        "content": {"title": "", "description": ""},
                    },
                }
            },
            {
                "item": {
                    "id": "pi-network",
                    "coin_id": 0,
                    "name": "Pi Network",
                    "symbol": "PI",
                    "market_cap_rank": 41,
                    "thumb": "",
                    "small": "",
                    "large": "",
                    "slug": "",
                    "price_btc": 0,
                    "score": 0,
                    "data": {
                        "price": 0,
                        "price_btc": "",
                        "price_change_percentage_24h": {"usd": -0.01},
                        "market_cap": "",
                        "market_cap_btc": "",
                        "total_volume": "",
                        "total_volume_btc": "",
                        "sparkline": "",
                        "content": {"title": "", "description": ""},
                    },
                }
            },
            {
                "item": {
                    "id": "pudgy-penguins",
                    "coin_id": 0,
                    "name": "Pudgy Penguins",
                    "symbol": "PENGU",
                    "market_cap_rank": 107,
                    "thumb": "",
                    "small": "",
                    "large": "",
                    "slug": "",
                    "price_btc": 0,
                    "score": 0,
                    "data": {
                        "price": 0,
                        "price_btc": "",
                        "price_change_percentage_24h": {"usd": -0.22},
                        "market_cap": "",
                        "market_cap_btc": "",
                        "total_volume": "",
                        "total_volume_btc": "",
                        "sparkline": "",
                        "content": {"title": "", "description": ""},
                    },
                }
            },
            {
                "item": {
                    "id": "neiro-3",
                    "coin_id": 0,
                    "name": "Neiro",
                    "symbol": "NEIRO",
                    "market_cap_rank": 670,
                    "thumb": "",
                    "small": "",
                    "large": "",
                    "slug": "",
                    "price_btc": 0,
                    "score": 0,
                    "data": {
                        "price": 0,
                        "price_btc": "",
                        "price_change_percentage_24h": {"usd": 3.12},
                        "market_cap": "",
                        "market_cap_btc": "",
                        "total_volume": "",
                        "total_volume_btc": "",
                        "sparkline": "",
                        "content": {"title": "", "description": ""},
                    },
                }
            },
            {
                "item": {
                    "id": "solana",
                    "coin_id": 0,
                    "name": "Solana",
                    "symbol": "SOL",
                    "market_cap_rank": 7,
                    "thumb": "",
                    "small": "",
                    "large": "",
                    "slug": "",
                    "price_btc": 0,
                    "score": 0,
                    "data": {
                        "price": 0,
                        "price_btc": "",
                        "price_change_percentage_24h": {"usd": -0.12},
                        "market_cap": "",
                        "market_cap_btc": "",
                        "total_volume": "",
                        "total_volume_btc": "",
                        "sparkline": "",
                        "content": {"title": "", "description": ""},
                    },
                }
            },
            {
                "item": {
                    "id": "ethereum",
                    "coin_id": 0,
                    "name": "Ethereum",
                    "symbol": "ETH",
                    "market_cap_rank": 2,
                    "thumb": "",
                    "small": "",
                    "large": "",
                    "slug": "",
                    "price_btc": 0,
                    "score": 0,
                    "data": {
                        "price": 0,
                        "price_btc": "",
                        "price_change_percentage_24h": {"usd": -4.15},
                        "market_cap": "",
                        "market_cap_btc": "",
                        "total_volume": "",
                        "total_volume_btc": "",
                        "sparkline": "",
                        "content": {"title": "", "description": ""},
                    },
                }
            },
            {
                "item": {
                    "id": "hyperliquid",
                    "coin_id": 0,
                    "name": "Hyperliquid",
                    "symbol": "HYPE",
                    "market_cap_rank": 16,
                    "thumb": "",
                    "small": "",
                    "large": "",
                    "slug": "",
                    "price_btc": 0,
                    "score": 0,
                    "data": {
                        "price": 0,
                        "price_btc": "",
                        "price_change_percentage_24h": {"usd": 3.88},
                        "market_cap": "",
                        "market_cap_btc": "",
                        "total_volume": "",
                        "total_volume_btc": "",
                        "sparkline": "",
                        "content": {"title": "", "description": ""},
                    },
                }
            },
        ]
    }


@pytest.fixture
def sample_market_response():
    return [
        {
            "id": "bitcoin",
            "symbol": "BTC",
            "name": "Bitcoin",
            "image": "",
            "current_price": 67883,
            "market_cap": 1358579644402,
            "market_cap_rank": 0,
            "fully_diluted_valuation": 0,
            "total_volume": 0,
            "high_24h": 0,
            "low_24h": 0,
            "price_change_24h": 712.43,
            "price_change_percentage_24h": 0,
            "market_cap_change_24h": 0,
            "market_cap_change_percentage_24h": 0,
            "circulating_supply": 0,
            "total_supply": 0,
            "max_supply": None,
            "ath": 0,
            "ath_change_percentage": 0,
            "ath_date": "",
            "atl": 0,
            "atl_change_percentage": 0,
            "atl_date": "",
            "roi": None,
            "last_updated": "",
        },
        {
            "id": "ethereum",
            "symbol": "ETH",
            "name": "Ethereum",
            "image": "",
            "current_price": 2010.05,
            "market_cap": 242492427291,
            "market_cap_rank": 0,
            "fully_diluted_valuation": 0,
            "total_volume": 0,
            "high_24h": 0,
            "low_24h": 0,
            "price_change_24h": 61.27,
            "price_change_percentage_24h": 0,
            "market_cap_change_24h": 0,
            "market_cap_change_percentage_24h": 0,
            "circulating_supply": 0,
            "total_supply": 0,
            "max_supply": None,
            "ath": 0,
            "ath_change_percentage": 0,
            "ath_date": "",
            "atl": 0,
            "atl_change_percentage": 0,
            "atl_date": "",
            "roi": None,
            "last_updated": "",
        },
        {
            "id": "solana",
            "symbol": "SOL",
            "name": "Solana",
            "image": "",
            "current_price": 84.32,
            "market_cap": 48136347807,
            "market_cap_rank": 0,
            "fully_diluted_valuation": 0,
            "total_volume": 0,
            "high_24h": 0,
            "low_24h": 0,
            "price_change_24h": 1.71,
            "price_change_percentage_24h": 0,
            "market_cap_change_24h": 0,
            "market_cap_change_percentage_24h": 0,
            "circulating_supply": 0,
            "total_supply": 0,
            "max_supply": None,
            "ath": 0,
            "ath_change_percentage": 0,
            "ath_date": "",
            "atl": 0,
            "atl_change_percentage": 0,
            "atl_date": "",
            "roi": None,
            "last_updated": "",
        },
    ]


# ---------------------------------------------------------------------------
# Parsed model fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_coin_price():
    return CoinPrice(
        coin_id="bitcoin",
        currency="usd",
        price=66060.0,
        change_24h=-1.79,
    )


@pytest.fixture
def sample_trending_coins():
    return [
        TrendingCoin(coin_id="bitcoin", name="Bitcoin", symbol="BTC", market_cap_rank=1, change_24h=0.58),
        TrendingCoin(coin_id="bittensor", name="Bittensor", symbol="TAO", market_cap_rank=45, change_24h=0.30),
        TrendingCoin(coin_id="pi-network", name="Pi Network", symbol="PI", market_cap_rank=41, change_24h=-0.01),
        TrendingCoin(coin_id="pudgy-penguins", name="Pudgy Penguins", symbol="PENGU", market_cap_rank=107, change_24h=-0.22),
        TrendingCoin(coin_id="neiro-3", name="Neiro", symbol="NEIRO", market_cap_rank=670, change_24h=3.12),
        TrendingCoin(coin_id="solana", name="Solana", symbol="SOL", market_cap_rank=7, change_24h=-0.12),
        TrendingCoin(coin_id="ethereum", name="Ethereum", symbol="ETH", market_cap_rank=2, change_24h=-4.15),
    ]


@pytest.fixture
def sample_coin_markets():
    return [
        CoinMarket(
            coin_id="bitcoin",
            name="Bitcoin",
            symbol="BTC",
            current_price=67883.0,
            market_cap=1358579644402.0,
            change_24h=712.43,
        ),
        CoinMarket(
            coin_id="ethereum",
            name="Ethereum",
            symbol="ETH",
            current_price=2010.05,
            market_cap=242492427291.0,
            change_24h=61.27,
        ),
        CoinMarket(
            coin_id="solana", name="Solana", symbol="SOL", current_price=84.32, market_cap=48136347807.0, change_24h=1.71
        ),
    ]


# ---------------------------------------------------------------------------
# Mock client fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_coingecko_client(sample_coin_price, sample_trending_coins, sample_coin_markets):
    client = AsyncMock(spec=CoinGeckoClient)
    client.get_price.return_value = sample_coin_price
    client.get_trending.return_value = sample_trending_coins
    client.get_market.return_value = sample_coin_markets
    return client
