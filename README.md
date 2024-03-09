# fastapi-oauth-mongo-react-starter

When building MVPs it's great to find some pre-setup boilerplate.   
This starter kit is based on https://github.com/gaganpreet/fastapi-starter but with some improvements

### Changes
- PostgreSQL replaced with MongoDB and Beanie ODM<br>
<em>Which makes it even more useful for MVPs and startups :) </em><br>
<em>Conversion implemented using Cursor IDE (https://cursor.sh/) - it's really nice way to rewrite code using AI, recommend</em>
- Added full Google OAuth authentication flow based on https://fastapi-users.github.io/fastapi-users/latest/configuration/oauth/ <br>
<em>Was surprised, that there are not much documentation how to make full integration using fastapi-users and React frontend, so here it is</em>

## Features

- FastAPI
- FastAPI Users with Google OAuth
- React Admin
- MongoDB and Beanie ODM
- Pre-commit hooks (black, autoflake, isort, flake8, prettier)
- Github Action
- Docker images


## Step 1: Getting started

Copy env-template to .env file and setup appropriate secrets
Start a local development instance with docker-compose

```bash
docker compose up
```

Now you can navigate to the following URLs:

- Backend OpenAPI docs: http://localhost:8000/docs/
- Frontend: http://localhost:3000

### Step 2: Local development

You can start all services separately. For example run mongodb:
```bash
docker compose up mongodb
```

The backend setup of docker compose is set to automatically reload the app whenever code is updated. 
But for example you can always debug `python main.py` with PyCharm

To develop frontend:
```bash
cd frontend
yarn
yarn start
```

If you want to develop against something other than the default host, localhost:8000, you can set the `REACT_APP_API_BASE` environment variable:

```bash
export REACT_APP_API_BASE=http://mydomain.name:8000
yarn start
```

Don't forget to edit the `.env` file and update the `BACKEND_CORS_ORIGINS` value (add `http://mydomain:3000` to the allowed origins).

### Step 3: Pre-commit hooks

Keep your code clean by using the configured pre-commit hooks. Follow the [instructions here to install pre-commit](https://pre-commit.com/). Once pre-commit is installed, run this command to install the hooks into your git repository:

```bash
pre-commit install
```

Run all pre-commit hooks:
```
pre-commit run -a
```

### Step 4: Local tests
Frontend:
```bash
cd frontend
yarn test
```
Backend:
```bash
cd backend
pytest tests
```

### Rebuilding containers

If you add a dependency, you'll need to rebuild your containers like this:

```bash
docker compose up -d --build
```

### Regenerate front-end API package

Instead of writing frontend API client manually, OpenAPI Generator is used. Typescript bindings for the backend API can be recreated with this command:

```bash
yarn genapi
```

### Backend tests

The `Backend` service uses a hardcoded database named `apptest`. First, ensure that it's created

Then you can run tests with this command:

```bash
 docker compose up backend
 docker compose exec -T backend pytest -v --cov --cov-report term-missing
```

### Single docker image

There's a monolith/single docker image that uses FastAPI to serve static assets. You can use this image to deploy directly to Heroku, Fly.io or anywhere where you can run a Dockerfile without having to build a complicated setup out of separate frontend and backend images.

### Recipes

#### Build and upload docker images to a repository

Configure the [**build-push-action**](https://github.com/marketplace/actions/build-and-push-docker-images) in `.github/workflows/test.yaml`.

### Good to know

The frontend of this project uses React Admin. Follow the quick tutorial to understand how [React Admin](https://marmelab.com/react-admin/Tutorial.html) works.
