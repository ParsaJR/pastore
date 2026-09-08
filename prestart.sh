#!/usr/bin/env bash

set -e

export UV_NO_DEV=true

uv run alembic -c ./app/alembic.ini upgrade head
