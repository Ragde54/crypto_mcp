from __future__ import annotations

from httpx import AsyncClient, HTTPStatusError

from crypto_mcp.config import settings
from crypto_mcp.models.crypto import CoinMarket, CoinPrice, TrendingCoin


class CoinGeckoClient:
    def __init__(self):
        self.settings = settings
        
    async def __aenter__(self):
        self.client = AsyncClient()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def get_price(self, coin_id: str, currency: str) -> CoinPrice:
        url = f"{self.settings.coingecko_base_url}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": currency,
            "include_24hr_change": True,
        }
        headers = {
            "x-cg-demo-api-key": self.settings.coingecko_api_key,
        }
        data={}
        try:
            response = await self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Coin '{coin_id}' not found")
            if e.response.status_code == 429:
                raise ValueError("Rate limit exceeded, try again later")
            raise
    
        return CoinPrice.from_api_response(
            data=data,
            coin_id=coin_id,
            currency=currency,
        )
    
    async def get_trending(self) -> list[TrendingCoin]:
        url = f"{self.settings.coingecko_base_url}/search/trending"
        headers={"x-cg-demo-api-key": self.settings.coingecko_api_key}
        data={}
        try:
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("Trending coins not found")
            if e.response.status_code == 429:
                raise ValueError("Rate limit exceeded, try again later")
            raise
        return [TrendingCoin.from_api_response(coin) for coin in data["coins"]]

    async def get_market_overview(self, currency: str, top_n: int = 10) -> list[CoinMarket]:
        url = f"{self.settings.coingecko_base_url}/coins/markets"
        params = {
            "vs_currency": currency,
            "order": "market_cap_desc",
            "per_page": top_n,
        }
        headers={"x-cg-demo-api-key": self.settings.coingecko_api_key}
        data={} 
        try:
            response = await self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("Markets not found")
            if e.response.status_code == 429:
                raise ValueError("Rate limit exceeded, try again later")
            raise
        return [CoinMarket.from_api_response(coin) for coin in data]