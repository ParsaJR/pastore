## Pastore

A pastebin service that you can actually own. 

Scroll down the README for some [pretty gifs](#animated_gifs)

## (Non-)Features

- A good looking web client, powered by [Vue.JS](https://vuejs.org) & [Nuxt UI](https://ui.nuxt.com/)
- Beautiful syntax highlighting, powered by [Shiki](https://shiki.style/)
- Automatic language detecting powered by [Flourite](https://github.com/teknologi-umum/flourite) 
- Administration capabilities
- Opt-in caching, powered by [Redis.py](https://github.com/redis/redis-py)



## Deployment

#### Docker-compose

Create a `docker-compose.yml` file with the following contents:

```yaml
x-common-env: &common-env
  PASTORE_JWT_SECRET: supersecret
  PASTORE_INITIAL_ADMIN_PASSWORD: supersecret

  PASTORE_DATABASE_HOST: db
  PASTORE_DATABASE_NAME: &db_name pastore
  PASTORE_DATABASE_PASSWORD: &db_password changeme
  PASTORE_DATABASE_USERNAME: &db_user pastore

  # Optional
  PASTORE_LOG_STRUCTURED: False
  PASTORE_LOG_LEVEL: info

  # Optional
  PASTORE_Metrics_Enabled: False
  PASTORE_Metrics_Username: "pastore" 
  PASTORE_Metrics_Password: "secret"
  
  
  # Optional
  PASTORE_REDIS_ENABLED: False
  PASTORE_REDIS_HOST: 127.0.0.1
  PASTORE_REDIS_PORT: 6379
  PASTORE_REDIS_PASSWORD: secret


services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
        POSTGRES_PASSWORD: *db_password
        POSTGRES_USER: *db_user
        POSTGRES_DB: *db_name
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB
      interval: 10s
      timeout: 3s
      retries: 3


  migrate:
    image: parsajr/pastore
    command: uv run alembic -c ./app/alembic.ini upgrade head
    environment:
        <<: *common-env
    depends_on:
      db:
        condition: service_healthy
    restart: "no"

  api:
    image: parsajr/pastore
    environment:
        <<: *common-env

    depends_on: 
      migrate:
        condition: service_completed_successfully
    ports:
      - "8080:80"
    restart: unless-stopped

volumes:
  postgres-data:

```

It defines three services:

- A PostgreSQL database container `db` which stores all the persistent data.

- A migration service that runs off the alembic migration script to make the
  database schema ready to consume for the api.

- Api service which runs the Pastore api and hosts its frontend client.


After that, your service is ready to be served at port 8080.

<!-- > [!IMPORTANT] -->
<!-- > As for now, You need to reverse proxy the api service under the location -->
<!-- > "/api" in the same origin as where the frontend service has served. Just like -->
<!-- > the nginx configuration below: -->

<!-- >``` -->
<!-- >   server { -->
<!-- >       listen       80; -->
<!-- >       listen       [::]:80; -->
<!-- >       server_name  test.example.org; -->
<!-- > -->
<!-- >	location / { -->
<!-- >		proxy_pass http://localhost:8081; -->
<!-- >	} -->
<!-- > -->
<!-- >	location /api { -->
<!-- >		proxy_pass http://localhost:8080; -->
<!-- >	} -->
<!-- > -->
<!-- >  } -->

## Development

Make sure to install the following dependencies:

- [Mise](https://mise.jdx.dev/getting-started.html)
- [Docker & Docker Compose](https://docs.docker.com/get-started/)

This project uses `uv` and `pnpm` as a package manager toolkit for back-end
and front-end side, respectively.

Also, `just`, the command runner, defines some common development tasks to help
you get started.

All three of these should automatically be installed by `mise`.

1. Install the project's dependencies:

```sh
mise install
```

2. Use the `justfile` to help you get started:

```sh
just setup-api

just setup-db

just run-api
```

## Preview
<a name="animated_gifs"></a>
<img width="1280" height="600" alt="ezgif-8d9e6ab0af591b68" src="https://github.com/user-attachments/assets/72f5c62d-11e5-4863-b7de-5fcc3f01d3be" />


<!-- > -->
<!-- >``` -->
