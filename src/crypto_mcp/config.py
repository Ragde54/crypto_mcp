from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    coingecko_api_key: str
    coingecko_base_url: str = "https://api.coingecko.com/api/v3"
    default_currency: str = "usd"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
