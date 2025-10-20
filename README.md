# Doughjoe Sim

A FastAPI web application with Tailwind CSS styling.

## Prerequisites

- Python 3.12 or higher
- Node.js and pnpm (for Tailwind CSS)
- uv (Python package manager)

## Development Setup

### 1. Install Python Dependencies

```bash
uv sync
```

### 2. Install Node.js Dependencies

```bash
pnpm install
```

### 3. Build CSS

If you need to rebuild the Tailwind CSS:

```bash
npx tailwindcss -i static/css/input.css -o static/css/styles.css --watch
```

### 4. Run the Development Server

```bash
uv run fastapi dev main.py
```

The application will be available at `http://localhost:8000`

## Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for code formatting and linting.

### Running Ruff

Before pushing code, always run:

```bash
# Check for linting issues
uv run ruff check

# Format code
uv run ruff format
```

### Pre-push Workflow

Always ensure your code passes Ruff checks before pushing:

```bash
# Run both check and format
uv run ruff check && uv run ruff format
```

Ruff is configured as a development dependency and will help maintain consistent code style and catch potential issues.

