FROM python:3.8-slim-buster

EXPOSE 8000/tcp

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  DJANGO_SETTINGS_MODULE=datadrop.settings-prod

# System deps:
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code
VOLUME /static
VOLUME /data

CMD exec gunicorn datadrop.wsgi:application --bind 0.0.0.0:8000 --timeout 7200 --workers 3 --access-logfile=- --error-logfile=-
