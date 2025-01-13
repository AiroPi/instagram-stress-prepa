# syntax=docker/dockerfile-upstream:master-labs

FROM python:3.12-alpine AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    : \
    && uv sync --no-dev --locked \
    && :

FROM python:3.12-alpine AS base
# https://docs.docker.com/reference/dockerfile/#copy---parents
COPY --parents --from=build /app/.venv /
WORKDIR /app
COPY --parents ./resources .
COPY ./src .
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=0

FROM base AS production
CMD ["python",  "./main.py"]
