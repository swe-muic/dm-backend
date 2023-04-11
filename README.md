[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=swe-muic_dm-backend&metric=coverage)](https://sonarcloud.io/summary/new_code?id=swe-muic_dm-backend)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=swe-muic_dm-backend&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=swe-muic_dm-backend)

# Deezmoz: Online Graphing Calculator [Backend]

MUIC ICCS372 Software Engineering

# Repository Files

```
├── .github
│   └── workflow
│       ├── build.yml
│       └── lint.yml
├── dm_backend
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_equation_line_style.py
│   │   ├── 0003_graph_preview.py
│   │   ├── 0004_alter_equation_line_style.py
│   │   ├── 0005_alter_graph_owner.py
│   │   └── __init__.py
│   ├── src
│   │   ├── __init__.py
│   │   ├── dataclasses
│   │   │   └── __init__.py
│   │   ├── enums
│   │   │   ├── __init__.py
│   │   │   └── line_style_type.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── equation.py
│   │   │   └── graph.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   ├── equation.py
│   │   │   └── graph.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── api_renderer.py
│   │   └── views
│   │       ├── __init__.py
│   │       ├── equation.py
│   │       ├── equation_parser.py
│   │       └── graph.py
│   ├── tests
│   │   ├── baker_recipes
│   │   │   ├── __init__.py
│   │   │   ├── equation_baker_recipe.py
│   │   │   └── graph_baker_recipe.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── test_equation.py
│   │   │   └── test_graph.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   ├── test_equation.py
│   │   │   └── test_graph.py
│   │   └── views
│   │       ├── __init__.py
│   │       ├── test_equation.py
│   │       ├── test_equation_parser.py
│   │       └── test_graph.py
│   ├── .env.example
│   ├── asgi.py
│   ├── docker-compose.yml
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker
│   ├── build_docker.sh
│   └── run_docker.sh
├── Dockerfile
├── README.md
├── entrypoint.sh
├── manage.py
├── openapi.yml
├── poetry.lock
├── pyproject.toml
├── pytest.ini
├── sonar-project.properties
├── timeout_decorator-0.5.0-py3-none-any.whl
└── tox.ini
```

# Project Setup

Please run the following command to install required dependencies.
```
poetry install
```
<b> Note: </b> Please make sure <code>poetry</code> is installed on your machine.

Create a `.env` file following the same format of a `.env.example` file.

```
POSTGRES_USER =  username
POSTGRES_PASSWORD = password
POSTGRES_DB = postgres_db
MINIO_ROOT_USER = username
MINIO_ROOT_PASSWORD = password
```

<b> Note: </b> If MinIO is already set up on the frontend, then `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` can be omitted.

Please run `docker-compose up` to start a docker container

```
docker-compose up
```

<b> Note: </b> The current working directory <b> must be </b> where the file `docker-compose.yml` is located.

Finally, run the following commands
```
poetry run python manage.py migrate
poetry run python manage.py runserver
```

<b> Note: </b> The current working directory <b> must be </b> where the file `manage.py` is located.

# Run Tests

```
poetry run pytest
```

# APIs

APIs for communicating with backend

### Equations

List all existing equations
```
GET 	/api/viewset/equations/
```

Create a new equation
```
POST 	/api/viewset/equations/
```

Get an existing equation
```
GET 	/api/viewset/equations/{equation_id}/
```

Update an existing equation
```
PUT 	/api/viewset/equations/{equation_id}/
```

Delete an existing equation
```
DELETE 	/api/viewset/equations/{equation_id}/
```

### Equation Parser

Parse a given list expressions
```
POST /api/viewset/equations/parser/parse_expressions/
```

### Graphs

List all existing graphs
```
GET 	/api/viewset/graphs/
```

Create a new graph
```
POST 	/api/viewset/graphs/
```

Get an existing graph
```
GET 	/api/viewset/graphs/{graph_id}/
```

Update an existing graph
```
PUT 	/api/viewset/graphs/{graph_id}/
```

Delete an existing graph
```
DELETE 	/api/viewset/graphs/{graph_id}/
```

For more information, please checkout the `openapi.yml`.
