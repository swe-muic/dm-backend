FROM python:3.10-slim-bullseye

WORKDIR /app
ENV POETRY_VERSION=1.4.0 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1,

# Speeds up installation of Python packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends libpq-dev gcc build-essential \
    && pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --with gunicorn \
    && apt-get remove -y gcc build-essential \
    && apt-get autoremove -y

COPY manage.py entrypoint.sh ./
COPY dm_backend ./dm_backend

RUN poetry install \
    && chmod +x manage.py entrypoint.sh

EXPOSE 8000
ENTRYPOINT [ "./entrypoint.sh", "poetry", "run", "gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "dm_backend.asgi:application", "--timeout", "600", "--preload"]
