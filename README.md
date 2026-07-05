## Pastore

This is the repository of the Pastore pastebin service.


## (Non-)Features

✅ A good looking web client, powered by [Vue.JS](https://vuejs.org)
✅ Beautiful syntax highlighting, powered by [Shiki](https://shiki.style/)
✅ A language detector that is good enough, powered by [Flourite](https://github.com/teknologi-umum/flourite) 
✅ Administration capabilities



## Deployment

#### Docker-compose

Create a `docker-compose.yml` file with the following contents:

```yaml

x-common-env: &common-env
    PASTORE_JWT_SECRET: supersecret
    PASTORE_DATABASE_HOST: db
    PASTORE_DATABASE_PASSWORD: &db_password changeme
    PASTORE_DATABASE_USERNAME: &db_user pastore
    PASTORE_DATABASE_NAME: &db_name pastore

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
    image: pastore-local:v0.1
    command: uv run alembic -c ./app/alembic.ini upgrade head
    environment:
        <<: *common-env
    depends_on:
      db:
        condition: service_healthy
    restart: "no"

# REQUIRED: As for now, You need to Reverse proxy the api service under the
# location "/api", in the same origin as where frontend has served.
  api:
    image: pastore-local:v0.1
    environment:
        <<: *common-env

    depends_on: # Depends on the migration tasks that actually overrides the
    # main image api.
      migrate:
        condition: service_completed_successfully
    ports:
      - "8080:80"
    restart: unless-stopped

  frontend:
    image: parsajr/pastore-frontend:v0.1
    depends_on:
      api:
        condition: service_started
    ports:
      - "8081:8080"
    restart: unless-stopped

volumes:
  postgres-data:

```

It defines four services:

- A PostgreSQL database container `db` which stores all the persistent data.
- A migration service that runs off the alembic migration script, to make the
  database schema ready to use for the api.
- Api service which runs the Pastore api.

> [!IMPORTANT]
> As for now, You need to reverse proxy the api service under the location
> "/api" in the same origin as where the frontend service has served. Just like
> the nginx configuration below:

>```
>   server {
>       listen       80;
>       listen       [::]:80;
>       server_name  test.example.org;
>
>	location / {
>		proxy_pass http://localhost:8081;
>	}
>
>	location /api {
>		proxy_pass http://localhost:8080;
>	}
>
>  }
>
>```


- A frontend service that knows how to interact with the Pastore's api. As for
  now, it assumes your front-end is available at the "/api" of the same origin.






