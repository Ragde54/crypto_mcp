from __future__ import annotations

from pydantic import BaseModel


class CoinPrice(BaseModel):
    coin_id: str
    currency: str
    price: float
    change_24h: float | None

    @classmethod
    def from_api_response(cls, data: dict, coin_id: str, currency: str) -> CoinPrice:
        coin_data = data[coin_id]
        return cls(
            coin_id=coin_id,
            currency=currency,
            price=coin_data[currency],
            change_24h=coin_data.get(f"{currency}_24h_change")
    )

    def to_text(self) -> str:
        change = f"{round(self.change_24h, 2)}%" if self.change_24h is not None else "N/A"
        parts = [
            f"{self.coin_id.capitalize()} is {self.price} {self.currency.upper()}",
            f"24h change: {change}",
        ]
        return " | ".join(parts)

class TrendingCoin(BaseModel):
    coin_id: str
    name: str
    symbol: str
    market_cap_rank: int | None
    change_24h: float | None

    @classmethod
    def from_api_response(cls, data: dict) -> TrendingCoin:
        item = data["item"]
        return cls(
            coin_id=item["id"],
            name=item["name"],
            symbol=item["symbol"],
            market_cap_rank=item.get("market_cap_rank"),
            change_24h=item.get("data", {}).get("price_change_percentage_24h", {}).get("usd")
    )

    def to_text(self) -> str:
        change = f"{round(self.change_24h, 2)}%" if self.change_24h is not None else "N/A"
        rank = str(self.market_cap_rank) if self.market_cap_rank is not None else "N/A"
        parts = [
            f"{self.name} ({self.symbol.upper()})",
            f"Rank: {rank}",
            f"24h change: {change}",
        ]
        return " | ".join(parts)

class CoinMarket(BaseModel):
    coin_id: str
    name: str
    symbol: str
    current_price: float
    market_cap: float | None
    change_24h: float | None
    
    @classmethod
    def from_api_response(cls, data: dict) -> CoinMarket:
        return cls(
            coin_id=data["id"],
            name=data["name"],
            symbol=data["symbol"],
            current_price=data["current_price"],
            market_cap=data.get("market_cap"),
            change_24h=data.get("price_change_24h")
    )

    def to_text(self) -> str:
        change = f"{round(self.change_24h, 2)}%" if self.change_24h is not None else "N/A"
        parts = [
            f"{self.name} ({self.symbol.upper()})",
            f"Current price: {self.current_price}",
            f"Market cap: {self.market_cap}",
            f"24h change: {change}",
        ]
        return " | ".join(parts)