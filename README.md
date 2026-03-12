# Crypto MCP Server

[![CI Pipeline](https://github.com/Ragde54/crypto_mcp/actions/workflows/ci.yaml/badge.svg)](https://github.com/Ragde54/crypto_mcp/actions/workflows/ci.yaml)
[![Release](https://github.com/Ragde54/crypto_mcp/actions/workflows/release.yaml/badge.svg)](https://github.com/Ragde54/crypto_mcp/actions/workflows/release.yaml)

A production-ready [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol) server for interacting with cryptocurrency data via the CoinGecko API.

> Note: **This project is primarily for learning purposes.** It demonstrates how to build a production-ready, typed, tested, and containerized Python application using modern tooling (`uv`, `mypy`, `ruff`, GitHub Actions, Docker).

## 🌟 Features

- **MCP Integration**: Fully compliant with the Model Context Protocol, allowing AI assistants to natively query crypto data.
- **Production Grade Tooling**: Built with Astral's `uv` for lightning-fast dependency management.
- **Strict Typing & Linting**: Enforced via `mypy` strict mode and `ruff`.
- **Comprehensive Testing**: Unit and integration tests using `pytest` and `respx`.
- **Automated CI/CD**: GitHub Actions pipelines for running checks (CI) and automatically building/publishing Docker images to GHCR on tags (Release).
- **Containerized**: Distributable as a lightweight Docker image.

## 📁 Project Structure

```text
.
├── .github/workflows/      # CI/CD pipelines (ci.yaml, release.yaml)
├── src/
│   └── crypto_mcp/         # Main package payload
│       ├── clients/        # API clients (e.g., CoinGecko)
│       ├── models/         # Pydantic data models
│       ├── prompts/        # MCP Prompts
│       ├── tools/          # MCP Tools (get_price, get_trending, etc.)
│       ├── config.py       # Configuration management
│       └── server.py       # MCP Server initialization
├── tests/
│   ├── integration/        # Integration tests
│   └── unit/               # Unit tests
├── Dockerfile              # Multi-stage Docker build
├── Makefile                # Task runner (make check, make test)
└── pyproject.toml          # Project metadata and dependencies
```

## 🚀 Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) - An extremely fast Python package installer and resolver.
- Docker (optional, for containerized usage)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ragde54/crypto_mcp.git
   cd crypto_mcp
   ```

2. **Run tests and linters:**
   We use a standard Makefile target to run all quality checks (`ruff`, `mypy`, and `pytest`):
   ```bash
   make check
   ```

3. **Set up your environment:**
   Create a `.env` file in the root based on your needs. For the **free/demo** CoinGecko API, default settings usually suffice.

   > ⚠️ **Important API Key Note:**
   > By default, the application is configured to use the free public CoinGecko API. If you have a paid pro tier and want to use a real API key, you must modify the client headers. Specifically, update the header key from `x-cg-demo-api-key` to `x-cg-pro-api-key` (or whatever header is currently required by CoinGecko's premium tier) in `src/crypto_mcp/clients/coingecko.py`.

### Running the Server

#### Using UV
```bash
uv run python -m crypto_mcp.server
```

#### Using Docker
```bash
# Build the image locally
docker build -t crypto-mcp .

# Run the image
docker run --rm --env-file .env -i crypto-mcp
```

## 🤝 Contributing

Contributions are welcome! Please ensure any pull requests pass the CI pipeline (which runs `make check` on your code).