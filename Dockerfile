
# --- builder stage ---

FROM python:3.12-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-dev --no-install-project

COPY src/ ./src/

RUN uv sync --frozen --no-dev --no-editable

# --- runtime stage ---

FROM python:3.12-slim AS runtime

WORKDIR /app

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

COPY --from=builder /app/.venv /app/.venv

COPY --from=builder /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

CMD ["python", "-m", "crypto_mcp.server"]