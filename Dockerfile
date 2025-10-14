# First stage: dependency installation and build. Python shipped with OS will be used.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /project

ADD api api/
ADD app app/
ADD models models/
ADD pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Second stage: No uv installed, project files and virtual environment copied from the previous stage.
FROM python:3.12-slim-bookworm

WORKDIR /project

COPY --from=builder /project /project

# Append the executables from venv to PATH to ensure `uvicorn` is available.
ENV PATH="/project/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
