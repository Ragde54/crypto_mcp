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
                "coin_id": 1,
                "name": "Bitcoin",
                "symbol": "BTC",
                "market_cap_rank": 1,
                "thumb": "https://coin-images.coingecko.com/coins/images/1/standard/bitcoin.png?1696501400",
                "small": "https://coin-images.coingecko.com/coins/images/1/small/bitcoin.png?1696501400",
                "large": "https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png?1696501400",
                "slug": "bitcoin",
                "price_btc": 1.0,
                "score": 0,
                "data": {
                    "price": 69985.66517871761,
                    "price_btc": "1.0",
                    "price_change_percentage_24h": {"usd": 0.58},
                    "market_cap": "$1,399,077,267,893",
                    "market_cap_btc": "20000440.0",
                    "total_volume": "$58,017,631,390",
                    "total_volume_btc": "829141.9265441374",
                    "sparkline": "https://www.coingecko.com/coins/1/sparkline.svg",
                    "content": {
                        "title": "About Bitcoin (BTC)",
                        "description": "Bitcoin is the world's first decentralized cryptocurrency that enables peer-to-peer electronic cash transactions without intermediaries like banks or governments."
                    }
                }
            }
        },
        {
            "item": {
                "id": "bittensor",
                "coin_id": 28452,
                "name": "Bittensor",
                "symbol": "TAO",
                "market_cap_rank": 45,
                "thumb": "https://coin-images.coingecko.com/coins/images/28452/standard/ARUsPeNQ_400x400.jpeg?1696527447",
                "small": "https://coin-images.coingecko.com/coins/images/28452/small/ARUsPeNQ_400x400.jpeg?1696527447",
                "large": "https://coin-images.coingecko.com/coins/images/28452/large/ARUsPeNQ_400x400.jpeg?1696527447",
                "slug": "bittensor",
                "price_btc": 0.0028924751447339677,
                "score": 1,
                "data": {
                    "price": 202.39545412033922,
                    "price_btc": "0.002892475144733967",
                    "price_change_percentage_24h": {"usd": 0.3},
                    "market_cap": "$1,944,863,204",
                    "market_cap_btc": "27773.25932159668",
                    "total_volume": "$168,615,426",
                    "total_volume_btc": "2409.717797600403",
                    "sparkline": "https://www.coingecko.com/coins/28452/sparkline.svg",
                    "content": {
                        "title": "What is Bittensor?",
                        "description": "Bittensor is an open-source protocol that utilizes blockchain technology to create a decentralized machine learning network. This network enables machine learning models to train collaboratively and be rewarded in TAO according to the informational value they offer the collective. Additionally, Bittensor's TAO grants external access to users, allowing them to extract information from the network while tuning its activities to meet their needs. The ultimate vision of Bittensor is to create a market for artificial intelligence, allowing producers and consumers of this commodity to interact in a trustless, open, and transparent context. Bittensor provides a novel strategy for developing and distributing artificial intelligence technology, promoting open access/ownership, decentralized governance, and global access to computing power and innovation within an incentivized framework. The Bittensor network operates using two types of nodes, servers and validators, with assessments based on the value of their responses. Nodes that add value to the network are rewarded with more stake (TAO), while low-value nodes are weakened and eventually de-registered."
                    }
                }
            }
        },
        {
            "item": {
                "id": "pi-network",
                "coin_id": 54342,
                "name": "Pi Network",
                "symbol": "PI",
                "market_cap_rank": 41,
                "thumb": "https://coin-images.coingecko.com/coins/images/54342/standard/pi_network.jpg?1739347576",
                "small": "https://coin-images.coingecko.com/coins/images/54342/small/pi_network.jpg?1739347576",
                "large": "https://coin-images.coingecko.com/coins/images/54342/large/pi_network.jpg?1739347576",
                "slug": "pi-network",
                "price_btc": 3.199202122124248e-06,
                "score": 2,
                "data": {
                    "price": 0.2238580917484923,
                    "price_btc": "0.000003199202122124248",
                    "price_change_percentage_24h": {"usd": -0.01},
                    "market_cap": "$2,175,037,696",
                    "market_cap_btc": "31067.34344888242",
                    "total_volume": "$35,477,495",
                    "total_volume_btc": "507.0161992308922",
                    "sparkline": "https://www.coingecko.com/coins/54342/sparkline.svg",
                    "content": {
                        "title": "What Is Pi Network?",
                        "description": "Pi Network is a social cryptocurrency, developer platform, and ecosystem designed for widespread accessibility and real-world utility. It enables users to mine and transact Pi using a mobile-friendly interface while supporting applications built within its blockchain ecosystem."
                    }
                }
            }
        },
        {
            "item": {
                "id": "pudgy-penguins",
                "coin_id": 52622,
                "name": "Pudgy Penguins",
                "symbol": "PENGU",
                "market_cap_rank": 107,
                "thumb": "https://coin-images.coingecko.com/coins/images/52622/standard/PUDGY_PENGUINS_PENGU_PFP.png?1733809110",
                "small": "https://coin-images.coingecko.com/coins/images/52622/small/PUDGY_PENGUINS_PENGU_PFP.png?1733809110",
                "large": "https://coin-images.coingecko.com/coins/images/52622/large/PUDGY_PENGUINS_PENGU_PFP.png?1733809110",
                "slug": "pudgy-penguins",
                "price_btc": 9.992527036613318e-08,
                "score": 3,
                "data": {
                    "price": 0.007003337547279523,
                    "price_btc": "0.00000009992527036613318",
                    "price_change_percentage_24h": {"usd": -0.22},
                    "market_cap": "$440,331,009",
                    "market_cap_btc": "6291.803739171465",
                    "total_volume": "$132,493,365",
                    "total_volume_btc": "1890.446546707074",
                    "sparkline": "https://www.coingecko.com/coins/52622/sparkline.svg",
                    "content": {
                        "title": "PENGU is the official coin of Pudgy Penguins.",
                        "description": "Pudgy Penguins has become the face of crypto with one of the most influential communities in the industry. From large companies wearing the Penguin, to being featured in ETF commercials, to garnering millions of followers and over 100 billion views, the Pengu has become a cultural icon making PENGU the world’s social currency."
                    }
                }
            }
        },
        {
            "item": {
                "id": "neiro-3",
                "coin_id": 39488,
                "name": "Neiro",
                "symbol": "NEIRO",
                "market_cap_rank": 670,
                "thumb": "https://coin-images.coingecko.com/coins/images/39488/standard/neiro.jpg?1731449567",
                "small": "https://coin-images.coingecko.com/coins/images/39488/small/neiro.jpg?1731449567",
                "large": "https://coin-images.coingecko.com/coins/images/39488/large/neiro.jpg?1731449567",
                "slug": "neiro-3",
                "price_btc": 9.392883726838654e-10,
                "score": 4,
                "data": {
                    "price": 6.583073034515874e-05,
                    "price_btc": "0.0000000009392883726838654",
                    "price_change_percentage_24h": {"usd": 3.12},
                    "market_cap": "$27,717,434",
                    "market_cap_btc": "396.068436649025",
                    "total_volume": "$18,809,254",
                    "total_volume_btc": "268.3748709454658",
                    "sparkline": "https://www.coingecko.com/coins/39488/sparkline.svg",
                    "content": {
                        "title": "What is Neiro about?",
                        "description": "Neiro is an ERC-20 token deployed on Ethereum, dedicated to the newly-adopted Shiba Inu dog from the woman who previously owned the famous Kabosu, face of the Doge meme."
                    }
                }
            }
        },
        {
            "item": {
                "id": "solana",
                "coin_id": 4128,
                "name": "Solana",
                "symbol": "SOL",
                "market_cap_rank": 7,
                "thumb": "https://coin-images.coingecko.com/coins/images/4128/standard/solana.png?1718769756",
                "small": "https://coin-images.coingecko.com/coins/images/4128/small/solana.png?1718769756",
                "large": "https://coin-images.coingecko.com/coins/images/4128/large/solana.png?1718769756",
                "slug": "solana",
                "price_btc": 0.0012319719313246885,
                "score": 5,
                "data": {
                    "price": 86.20489581662594,
                    "price_btc": "0.001231971931324688",
                    "price_change_percentage_24h": {"usd": -0.12},
                    "market_cap": "$49,226,116,314",
                    "market_cap_btc": "703668.0260262468",
                    "total_volume": "$4,718,957,714",
                    "total_volume_btc": "67439.59717546619",
                    "sparkline": "https://www.coingecko.com/coins/4128/sparkline.svg",
                    "content": {
                        "title": "About Solana (SOL)",
                        "description": "Solana is a high-performance Layer 1 blockchain built for mass adoption, offering a fast and low-cost environment for decentralized applications."
                    }
                }
            }
        },
        {
            "item": {
                "id": "ethereum",
                "coin_id": 279,
                "name": "Ethereum",
                "symbol": "ETH",
                "market_cap_rank": 2,
                "thumb": "https://coin-images.coingecko.com/coins/images/279/standard/ethereum.png?1696501628",
                "small": "https://coin-images.coingecko.com/coins/images/279/small/ethereum.png?1696501628",
                "large": "https://coin-images.coingecko.com/coins/images/279/large/ethereum.png?1696501628",
                "slug": "ethereum",
                "price_btc": 0.029090669747131544,
                "score": 6,
                "data": {
                    "price": 2035.5643590766372,
                    "price_btc": "0.02909066974713154",
                    "price_change_percentage_24h": {"usd": -4.15},
                    "market_cap": "$245,980,120,138",
                    "market_cap_btc": "3516189.34294213",
                    "total_volume": "$25,932,169,896",
                    "total_volume_btc": "370601.984119063",
                    "sparkline": "https://www.coingecko.com/coins/279/sparkline.svg",
                    "content": {
                        "title": "About Ethereum",
                        "description": "Ethereum is a blockchain platform that enables developers to build and deploy smart contracts and decentralized applications, operating through thousands of independent nodes worldwide rather than through a central authority."
                    }
                }
            }
        },
        {
            "item": {
                "id": "hyperliquid",
                "coin_id": 50882,
                "name": "Hyperliquid",
                "symbol": "HYPE",
                "market_cap_rank": 16,
                "thumb": "https://coin-images.coingecko.com/coins/images/50882/standard/hyperliquid.jpg?1729431300",
                "small": "https://coin-images.coingecko.com/coins/images/50882/small/hyperliquid.jpg?1729431300",
                "large": "https://coin-images.coingecko.com/coins/images/50882/large/hyperliquid.jpg?1729431300",
                "slug": "hyperliquid",
                "price_btc": 0.00048373536995952423,
                "score": 7,
                "data": {
                    "price": 33.84846367833975,
                    "price_btc": "0.0004837353699595242",
                    "price_change_percentage_24h": {"usd": 3.88},
                    "market_cap": "$8,066,845,669",
                    "market_cap_btc": "115271.2400258133",
                    "total_volume": "$414,745,351",
                    "total_volume_btc": "5927.211277438808",
                    "sparkline": "https://www.coingecko.com/coins/50882/sparkline.svg",
                    "content": {
                        "title": "What is Hyperliquid about?",
                        "description": "Hyperliquid is a performant L1 optimized from the ground up. The vision is a fully on-chain open financial system with user-built applications interfacing with performant native components, all without compromising end-user experience."
                    }
                }
            }
        }
    ]
}


@pytest.fixture
def sample_market_response():
    return [
        {
            "id": "bitcoin",
            "symbol": "BTC",
            "name": "Bitcoin",
            "image": "https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png?1696501400",
            "current_price": 67883,
            "market_cap": 1358579644402,
            "market_cap_rank": 1,
            "fully_diluted_valuation": 1358579644402,
            "total_volume": 41758097866,
            "high_24h": 68110,
            "low_24h": 65727,
            "price_change_24h": 712.43,
            "price_change_percentage_24h": 1.06062,
            "market_cap_change_24h": 14493725350,
            "market_cap_change_percentage_24h": 1.07833,
            "circulating_supply": 19999756.0,
            "total_supply": 19999756.0,
            "max_supply": 21000000.0,
            "ath": 126080,
            "ath_change_percentage": -46.1586,
            "ath_date": "2025-10-06T18:57:42.558Z",
            "atl": 67.81,
            "atl_change_percentage": 100009.38182,
            "atl_date": "2013-07-06T00:00:00.000Z",
            "roi": None,
            "last_updated": "2026-03-09T05:55:01.275Z",
        },
        {
            "id": "ethereum",
            "symbol": "ETH",
            "name": "Ethereum",
            "image": "https://coin-images.coingecko.com/coins/images/279/large/ethereum.png?1696501628",
            "current_price": 2010.05,
            "market_cap": 242492427291,
            "market_cap_rank": 2,
            "fully_diluted_valuation": 242492427291,
            "total_volume": 20311506013,
            "high_24h": 2009.86,
            "low_24h": 1922.33,
            "price_change_24h": 61.27,
            "price_change_percentage_24h": 3.14411,
            "market_cap_change_24h": 7137929309,
            "market_cap_change_percentage_24h": 3.03284,
            "circulating_supply": 120692044.84,
            "total_supply": 120692044.84,
            "max_supply": None,
            "ath": 4946.05,
            "ath_change_percentage": -59.36045,
            "ath_date": "2025-08-24T19:21:03.333Z",
            "atl": 0.432979,
            "atl_change_percentage": 464137.85292,
            "atl_date": "2015-10-20T00:00:00.000Z",
            "roi": None,
            "last_updated": "2026-03-09T05:55:00.737Z",
        },
        {
            "id": "solana",
            "symbol": "SOL",
            "name": "Solana",
            "image": "https://coin-images.coingecko.com/coins/images/4128/large/solana.png?1718769756",
            "current_price": 84.32,
            "market_cap": 48136347807,
            "market_cap_rank": 7,
            "fully_diluted_valuation": 48136353306,
            "total_volume": 3265824317,
            "high_24h": 84.19,
            "low_24h": 81.03,
            "price_change_24h": 1.71,
            "price_change_percentage_24h": 2.07314,
            "market_cap_change_24h": 993449297,
            "market_cap_change_percentage_24h": 2.10731,
            "circulating_supply": 570675712.09,
            "total_supply": 570675777.28,
            "max_supply": None,
            "ath": 293.31,
            "ath_change_percentage": -71.25112,
            "ath_date": "2025-01-19T11:15:27.957Z",
            "atl": 0.500801,
            "atl_change_percentage": 16737.8004,
            "atl_date": "2020-05-11T19:35:23.449Z",
            "roi": None,
            "last_updated": "2026-03-09T05:55:07.167Z",
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
def sample_trending_coin():
    return TrendingCoin(
        coin_id="bitcoin",
        name="Bitcoin",
        symbol="BTC",
        market_cap_rank=1,
        change_24h=0.58,
    )


@pytest.fixture
def sample_coin_market():
    return CoinMarket(
        coin_id="bitcoin",
        name="Bitcoin",
        symbol="btc",
        current_price=67883.0,
        market_cap=1358579644402.0,
        change_24h=712.43,
    )


# ---------------------------------------------------------------------------
# Mock client fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_coingecko_client(sample_coin_price, sample_trending_coin, sample_coin_market):
    client = AsyncMock(spec=CoinGeckoClient)
    client.get_price.return_value = sample_coin_price
    client.get_trending.return_value = [sample_trending_coin]
    client.get_market_overview.return_value = [sample_coin_market]
    return client