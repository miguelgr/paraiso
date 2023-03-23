# Cine Paraiso

> **Warning**
>
> **WORK in PROGRESS**

## Quickstart.

### Installation

Requires [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)


`docker-compose build`

`docker-compose up`

The site will be running in <a href="http://localhost:8000"> `http://localhost:8000`</a>
and the API in <a href="http://localhost:8000/api/v0"> `http://localhost:8000/api/v0`</a>

The `.env` file should be the main  configuration file for all the services.

### Database Configuration

For debugging purposes or to trigger django-admin commands, open a bash session in the service container.

`docker-compose run service bash`

To access the ADMIN site -> **Run this once**  Configure superuser for [Django's Admin Site](http://localhost:9000/admin)

`python manage createsuper user`
