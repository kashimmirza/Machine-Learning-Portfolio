# AgentPay - Awesome Agent API

A multi-agent system using FastAPI and React that integrates with the MNEE stablecoin for programmable money and AI agent payments.

## Project Structure

```
awesome-agent-api/
├── api/                    # FastAPI application
│   ├── db/                # Database models
│   ├── main.py            # Main API endpoints
│   └── models.py          # Pydantic schemas
├── application/           # Application services
│   └── chat_service/      # Agent service
├── infrastructure/        # Infrastructure code
│   ├── mnee_abi.json     # MNEE token ABI
│   └── web3_service.py   # Web3 integration
├── src/awesome_agent_api/ # Core logic
├── tests/                 # Tests
├── Dockerfile
├── docker-compose.yaml
└── pyproject.toml
```

## Setup

### Prerequisites
- Python 3.11+
- Poetry
- Docker (optional)
- PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   cd agent-pay/awesome-agent-api
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run with Docker Compose**
   ```bash
   docker-compose up
   ```

   Or run locally:
   ```bash
   make run
   ```

## API Endpoints

### Health Check
```http
GET /health
```

### Create Task
```http
POST /tasks
Content-Type: application/json

{
  "description": "Analyze market data",
  "price_mnee": 10.5
}
```

### Get Task
```http
GET /tasks/{task_id}
```

### Verify Payment
```http
POST /payments/verify
Content-Type: application/json

{
  "task_id": 1,
  "transaction_hash": "0x...",
  "sender_address": "0x..."
}
```

## MNEE Integration

This project uses the MNEE stablecoin (USD-backed) on Ethereum:
- **Contract Address**: `0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF`
- **Network**: Ethereum Mainnet
- **Decimals**: 6

## Development

```bash
# Run tests
make test

# Clean cache
make clean
```

## Frontend

The frontend is located in `../packages/web` and uses:
- Next.js
- RainbowKit for wallet connection
- Wagmi for Web3 interactions
- TailwindCSS for styling

## License

MIT
