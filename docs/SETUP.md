# Developer Setup Guide

## Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- Docker and Docker Compose (for containerized deployment)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/thanhauco/full-ai-agents.git
cd full-ai-agents
```

### 2. Install Dependencies

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys and configuration
nano .env
```

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `PINECONE_API_KEY`: Your Pinecone API key (for vector storage)

### 4. Set Up Pre-commit Hooks

```bash
poetry run pre-commit install
```

## Running the Application

### Local Development

```bash
# Run with uvicorn
poetry run uvicorn src.ai_agent.api.app:create_app --factory --reload --host 0.0.0.0 --port 8000
```

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f ai-agent

# Stop services
docker-compose down
```

## Running Tests

### All Tests

```bash
poetry run pytest
```

### With Coverage

```bash
poetry run pytest --cov=src/ai_agent --cov-report=html
```

### Property-Based Tests Only

```bash
poetry run pytest tests/test_properties_*.py -v
```

### Specific Test File

```bash
poetry run pytest tests/test_models.py -v
```

## Code Quality

### Format Code

```bash
poetry run black src tests
```

### Lint Code

```bash
poetry run ruff check src tests
```

### Type Check

```bash
poetry run mypy src
```

### Run All Quality Checks

```bash
poetry run black src tests
poetry run ruff check src tests --fix
poetry run mypy src
poetry run pytest
```

## Project Structure

```
.
├── src/ai_agent/          # Main application code
│   ├── api/               # FastAPI routes and app
│   ├── llm/               # LLM provider integrations
│   ├── memory/            # Memory management
│   ├── prompts/           # Prompt templates
│   ├── models.py          # Data models
│   └── config.py          # Configuration
├── tests/                 # Test suite
├── config/                # Configuration files
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD pipelines
├── pyproject.toml         # Project dependencies
├── Dockerfile             # Docker configuration
└── docker-compose.yml     # Multi-container setup
```

## Development Workflow

1. Create a feature branch
2. Make changes
3. Run tests and quality checks
4. Commit changes (pre-commit hooks will run automatically)
5. Push and create pull request

## Troubleshooting

### Poetry Installation Issues

If Poetry installation fails, try:
```bash
pip install poetry
```

### Docker Build Issues

Clear Docker cache:
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Test Failures

Ensure all dependencies are installed:
```bash
poetry install --with dev
```

## Additional Resources

- [API Documentation](API.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Architecture Overview](../README.md)
