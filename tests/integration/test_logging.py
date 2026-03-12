import json
import logging
from unittest.mock import AsyncMock, patch

import pytest

from crypto_mcp.logging import setup_logging
from crypto_mcp.server import call_tool, list_resources, read_resource


@pytest.fixture(autouse=True)
def configure_logging():
    setup_logging(level=logging.INFO)


@pytest.mark.asyncio
async def test_resource_endpoints():
    resources = await list_resources()
    assert len(resources) == 1
    assert str(resources[0].uri) == "info://crypto-mcp/version"

    res = await read_resource("info://crypto-mcp/version")
    parsed = json.loads(res)
    assert parsed["name"] == "crypto-mcp"
    assert "version" in parsed


@pytest.mark.asyncio
async def test_tool_logging_success(caplog, mock_coingecko_client, sample_coin_price):
    with caplog.at_level(logging.INFO):
        with patch(
            "crypto_mcp.tools.price.CoinGeckoClient",
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_coingecko_client), __aexit__=AsyncMock(return_value=False)
            ),
        ):
            await call_tool("get_price", {"coin_id": "bitcoin"})

    success_log = next((r for r in caplog.records if r.message == "Tool call successful"), None)
    assert success_log is not None
    assert success_log.tool_name == "get_price"  # type: ignore[attr-defined]
    assert success_log.coin_id == "bitcoin"  # type: ignore[attr-defined]
    assert success_log.success is True  # type: ignore[attr-defined]
    assert hasattr(success_log, "latency_ms")


@pytest.mark.asyncio
async def test_tool_logging_failure(caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="coin_id is required"):
            await call_tool("get_price", {})

    failure_log = next((r for r in caplog.records if r.message == "Tool call failed"), None)
    assert failure_log is not None
    assert failure_log.tool_name == "get_price"  # type: ignore[attr-defined]
    assert failure_log.coin_id is None  # type: ignore[attr-defined]
    assert failure_log.success is False  # type: ignore[attr-defined]
    assert hasattr(failure_log, "error")
