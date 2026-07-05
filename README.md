## Pastore

This is the repository of the Pastore pastebin service.


## (Non-)Features

✅ A good looking web client, powered by [Vue.JS](https://vuejs.org)
✅ Beautiful syntax highlighting, powered by [Shiki](https://shiki.style/)
✅ A language detector that is good enough, powered by [Flourite](https://github.com/teknologi-umum/flourite) 
✅ Administration capabilities



## Deployment

#### Docker-compose

Create a `docker-compose.yml` file with the
[https://github.com/ParsaJR/pastore/blob/main/docker-compose.yaml](following
contents).

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
  now, it assumes your front-end is available at the "/api" of the origin.






