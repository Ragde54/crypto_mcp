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