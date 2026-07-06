#############################################
# # Stage 1: Build the Pastore's vue client #
#############################################
ARG NODE_VERSION=22.22.0-alpine
ARG NGINX_VERSION=alpine3.23

FROM node:${NODE_VERSION} AS frontend

ENV CI="true"

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY web/package.json web/pnpm-lock.yaml web/pnpm-workspace.yaml ./

RUN corepack enable

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=.local/share/pnpm/store pnpm install

# Copy the rest of the application source code into the container
COPY web/ .

# Build the Vue.js application
RUN pnpm run build

# ############################################### #
#  Stage two. The combination of FastAPI & Vue  #
###################################################
FROM python:3.14-slim

## Installing uv
COPY --from=ghcr.io/astral-sh/uv:0.11.15 /uv /uvx /bin/

WORKDIR /app

COPY --from=frontend /app/dist ./dist

## Uv's dependency system
COPY pyproject.toml uv.lock ./

# System dependencies for psycopg2 package. Such a weird design by the author.
# I need to to everything in one overlay so the image size will be more optimal..
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && uv sync --frozen --no-dev \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

CMD ["uv", "run", "fastapi", "run", "./app/main.py", "--port", "80"]
