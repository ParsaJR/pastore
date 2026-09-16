#!/usr/bin/env bash

# This prestart script mainly exists because the app needs an explicit migration step before starting.

set -e

export UV_NO_DEV=true

uv run alembic -c ./app/alembic.ini upgrade head
