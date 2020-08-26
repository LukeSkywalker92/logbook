# LOGBOOK

Application for electronic Logbooks.

## Development on local machine (with SQLite database)

Prerequesites:
* python3
* pip
* virtualenv

Install requirements:
* activate virtual environment
* `cd app`
* `pip install -r requirements.txt`

Migrations:
* activate virtual environment
* `cd app`
* `cd app`
* `python manage.py makemigrations --settings=logbook.settings_dev`
* `python manage.py migrate --settings=logbook.settings_dev`

Running:
* activate virtual environment
* `cd app`
* `python manage.py runserver --settings=logbook.settings_dev`
* Access app at `127.0.0.1:8000` with your browser

## Development in docker container

Prerequesits:
* docker
* docker-compose

Build:
* set environment variables in `.env.dev`
* `docker-compose docker-compose.dev.yml build`

Running:
* `docker-compose docker-compose.dev.yml up` (add -d to detach the process from terminal)
* Access app at `127.0.0.1:8000` with your browser
* Standard admin credentials: `admin:admin`

## Deployment

Build:
* set environment variables in `.env`
* set strong `SECRET_KEY` in `.env`! (https://djecrety.ir/)
* `docker-compose build`

Running:
* `docker-compose up -d`
* Access app at `127.0.0.1:1337` with your browser or configure proxy to this port
* Standard admin credentials: `admin:admin`

