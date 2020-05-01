# DataDrop

## Features
- allow external user to upload files without account
- allow registered users to download uploaded files
- log registred users downloads
## Installation for prod

## Installation for dev
```bash
poetry install
poetry run ./manage.py migrate
poetry run ./manage.py createsuperuser
poetry run ./manage.py runserver
```


