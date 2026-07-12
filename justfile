set quiet

###########
# Project #
###########

[group('api')]
setup-env:
	#!/usr/bin/env bash
	cat > .env <<EOF
	PASTORE_JWT_SECRET=blasdadsajdasadflkjdsaflkl1123
	PASTORE_DEVELOPMENT=True
	EOF
	
# Install the vue project dependencies using pnpm toolkit.
[working-directory: 'web']
[group('vue')]
setup-vue:
	@pnpm install

# Install the FastAPI project dependencies using uv toolkit.
[group('api')]
setup-api:
	@uv sync

# Run projects in a single tmux session(splitting horizentally)
run-by-tmux:
	@tmux new-session -d -s dev -c web 'pnpm run dev' \; \
	split-window -h -t dev 'uv run fastapi dev' \; \
	attach -t dev


test-api:
	uv run pytest
	


# Run the vue project
[working-directory: 'web']
[group('global')]
run-vue:
	@pnpm run dev

# Run the FastAPI project
[group('global')]
run-api:
	@uv run fastapi dev

#############
# Database  #
#############

postgres_tag := "16-alpine"
postgres_password := "secret"
postgres_container_name := "pasted-postgres-dev"


# Run a postgres database container using docker toolkit, respecting the default configuration of the FastAPI project(variables can be overridden)
[group('api')]
setup-db:
	@docker volume create pgdata
	@docker run --detach \
		--name {{postgres_container_name}} \
		--volume pgdata:/var/lib/postgresql/data \
		-e POSTGRES_PASSWORD={{postgres_password}} \
		-p 127.0.0.1:5432:5432 \
		postgres:16-alpine

[group('api')]
run-db:
	@docker start {{postgres_container_name}}

# Stop the postgres container
[group('api')]
stop-db:
	@docker stop {{postgres_container_name}}

# Remove the postgres container 
[group('api')]
remove-db:
	@docker rm -f {{postgres_container_name}}

############
# Alembic  #
############

alembic_conf := "./app/alembic.ini"

# Create a new alembic migration, using the autogenerate feature.
[group('api-migration')]
alembic-new-migration message:
	@uv run alembic -c {{alembic_conf}} revision --autogenerate -m "{{message}}"

# Propagating all of the migration into the database
[group('api-migration')]
migrate:
	@uv run alembic -c {{alembic_conf}} upgrade head

# Rollback a alembic migration by one step
[group('api-migration')]
rollback:
	@uv run alembic -c {{alembic_conf}} downgrade -1
