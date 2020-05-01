# DataDrop
Easily get files from other people.

## Features
- allow external users to upload files without account (just send them the link)
- allow registered users to download uploaded files
- log registred users downloads

## Installation for prod
Build the Docker
```bash
./build-docker.sh
```

Edit *settings-prod.py* to setup your SMTP conf (or remove it)

Run the Docker
```bash
./run-docker.sh
docker exec -it datadrop ./manage.py migrate
docker exec -it datadrop ./manage.py collectstatic
docker exec -it datadrop ./manage.py createsuperuser
```

## Installation for dev
```bash
poetry install
poetry run ./manage.py migrate
poetry run ./manage.py createsuperuser
poetry run ./manage.py runserver
```


