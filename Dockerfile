FROM ghcr.io/astral-sh/uv:0.11-python3.14-alpine AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

FROM python:3.14-alpine

WORKDIR /app

# Required for GitPython
RUN apk add --no-cache git ca-certificates

COPY --from=builder /app/.venv /app/.venv

COPY *.py ./

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

CMD ["python", "nb-dt-import.py"]