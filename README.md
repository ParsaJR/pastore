## Pastore

A pastebin service that you can actually own. 

Scroll down the README for some [pretty gifs](#animated_gifs)

## Table of Contents

- [Features](#features)
  - [Web Client](#web-client)
  - [Syntax Highlighting](#syntax-highlighting)
  - [Administration](#administration)
  - [Caching](#caching)
  - [Metrics](#metrics)
- [Deployment](#deployment)
- [Configuration](#configuration)

# TLDR

- A good looking web client, powered by [Vue.JS](https://vuejs.org) & [Nuxt UI](https://ui.nuxt.com/)
- Beautiful syntax highlighting, powered by [Shiki](https://shiki.style/)
- Automatic language detecting powered by [Flourite](https://github.com/teknologi-umum/flourite) 
- Administration capabilities
- Opt-in caching, powered by [Redis.py](https://github.com/redis/redis-py)
- Metric exporter


## Web-client

Pastore provides a simple web interface, which is served by it's
backend. Pastore's Web-app stands on the shoulder of [Vue.JS](https://vuejs.org)
& [Nuxt UI](https://ui.nuxt.com/)

## Syntax highlighting

Pastore's web client provides a simple yet beautiful syntax highlighting,
powered by [Shiki](https://shiki.style/) and [Flourite](https://github.com/teknologi-umum/flourite)


## Administration

Just navigate to `/admin`, and then, things are easy to discover.

## Caching

The application is able to use redis as its caching solution, if you provide the
needed [configuration](#configuration).

## Metrics

The application is able to export some useful metrics, useful for getting an
insight. refer to [configuration](#configuration) section to see how to set it up.


## Configuration

Pastore can be configured through environment variables. All configuration
variables must be prefixed with `PASTORE_`.

During development, you can also use a .env file in the project's root
directory. Environment variables take precedence over values defined in the .env
file.

| Variable                         | Default   | Description                                            |
|----------------------------------|-----------|--------------------------------------------------------|
| `PASTORE_APP_NAME`               | `Pastore` | Application name. It will be displayed on your webapp. |
| `PASTORE_DEVELOPMENT`            | `false`   | Enable development mode.                               |
| `PASTORE_INITIAL_ADMIN_PASSWORD` | `None`    | Initial administrator password.                        |
	
### Database

Pastore uses PostgreSQL as its primary database. You'll need to set most of
these variables:

| Variable                    | Default     | Description                               |
|-----------------------------|-------------|-------------------------------------------|
| `PASTORE_DATABASE_HOST`     | `localhost` | PostgreSQL server hostname or IP address. |
| `PASTORE_DATABASE_PORT`     | `5432`      | PostgreSQL server port.                   |
| `PASTORE_DATABASE_USERNAME` | `postgres`  | Database username.                        |
| `PASTORE_DATABASE_PASSWORD` | `secret`    | Database password.                        |
| `PASTORE_DATABASE_NAME`     | `pasted`    | Database name.                            |

### Redis Caching

Redis is an optional dependency. If caching is not required, you can leave it disabled and run Pastore without Redis.

| Variable                 | Default     | Description                          |
|--------------------------|-------------|--------------------------------------|
| `PASTORE_REDIS_ENABLED`  | `false`     | Enable Redis-backed caching.         |
| `PASTORE_REDIS_HOST`     | `localhost` | Redis server hostname or IP address. |
| `PASTORE_REDIS_PORT`     | `6379`      | Redis server port.                   |
| `PASTORE_REDIS_PASSWORD` | Empty       | Redis authentication password.       |

### Prometheus Metrics

Pastore can expose application metrics for monitoring through Prometheus. The
authentication of the metrics endpoint is based on the simple [HTTP Basic Auth](https://en.wikipedia.org/wiki/Basic_access_authentication)

| Variable                   | Default | Description                             |
|----------------------------|---------|-----------------------------------------|
| `PASTORE_METRICS_ENABLED`  | `false` | Enable the metrics endpoint.            |
| `PASTORE_METRICS_USERNAME` | Empty   | Username for HTTP Basic Authentication. |
| `PASTORE_METRICS_PASSWORD` | Empty   | Password for HTTP Basic Authentication. |

### Authentication

Pastore uses JWT for authentication. Used for signing the tokens.

| Variable             | Default                 | Description                     |
|----------------------|-------------------------|---------------------------------|
| `PASTORE_JWT_SECRET` | Automatically generated | Secret used for signing JWTs.   |
| `PASTORE_JWT_TTL`    | `604800`(7 days!)       | JWT expiration time in seconds. |

**Important:** It is recommended to explicitly configure `PASTORE_JWT_SECRET` in
production. Otherwise, a new secret will be generated whenever the application
starts, invalidating previously issued tokens. 

### Logging

| Variable                 | Default | Description                                                     |
|--------------------------|---------|-----------------------------------------------------------------|
| `PASTORE_LOG_ENABLED`    | `true`  | Enable application logging.                                     |
| `PASTORE_LOG_STRUCTURED` | `false` | Enable structured logging.                                      |
| `PASTORE_LOG_LEVEL`      | `Debug` | Minimum logging level. Available options are `Info` and `Debug` |

### Example

Here is an example `.env` file with some commonly configured options:

```dotenv
PASTORE_DEVELOPMENT=false

# Initial administrator account
PASTORE_INITIAL_ADMIN_PASSWORD=change-me

# Database
PASTORE_DATABASE_HOST=localhost
PASTORE_DATABASE_PORT=5432
PASTORE_DATABASE_USERNAME=postgres
PASTORE_DATABASE_PASSWORD=your-database-password
PASTORE_DATABASE_NAME=pasted

# Redis (optional)
PASTORE_REDIS_ENABLED=true
PASTORE_REDIS_HOST=localhost
PASTORE_REDIS_PORT=6379

# Authentication
PASTORE_JWT_SECRET=replace-with-a-long-random-secret

# Prometheus metrics (optional)
PASTORE_METRICS_ENABLED=true
PASTORE_METRICS_USERNAME=prometheus
PASTORE_METRICS_PASSWORD=change-me

```

## Deployment

Pastore currently provides a ready-to-ship docker images at [Dockerhub](https://hub.docker.com/r/parsajr/pastore).

#### Docker-compose

Use the [docker-compose.yaml](docker-compose.yaml) file to setup the
service. Follow the instructions below:

1. Run the `prestart.sh` script. It sets up the migration for the database
schema:
```sh
docker compose run --rm api bash prestart.sh
```

2. Then, run the compose template in detached mode:
```sh
docker compose run -d
```

The compose template defines two services:

- A PostgreSQL database container `db` which stores all the persistent data.

- Api service which runs the Pastore api and hosts its front-end client.

After that, your service is ready to be served at port 8080. You can serve it
either directly, or by using a reverse proxy like Caddy or Nginx.

## Development

Make sure to install the following dependencies:

- [Mise](https://mise.jdx.dev/getting-started.html)
- [Docker & Docker Compose](https://docs.docker.com/get-started/)

This project uses `uv` and `pnpm` as a package manager toolkit for back-end
and front-end sides, respectively.

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

See the complete list of commands using `just --list`.

## Preview
<a name="animated_gifs"></a>
<img width="1280" height="600" alt="ezgif-8d9e6ab0af591b68" src="https://github.com/user-attachments/assets/72f5c62d-11e5-4863-b7de-5fcc3f01d3be" />
