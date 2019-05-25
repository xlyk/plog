# plog
Plog: the simple Python blog 

## Features
- Docker
- Python 3.7
- Flask
- Gunicorn for HTTP WSGI
- Mongo DB

## Required
Get the right version of Docker for your OS
- [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
- [Docker for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)

**Note:** The recommended requirement for deployment of this project is 4 GB RAM.
For Docker for Mac, this can be set by following these steps:

Open Docker > Preferences > Advanced tab, then set memory to 4.0 GiB

## Local setup
- In your root directory, copy your environment variable file
  - `cp env.dist .env`
  - **note:** set DEBUG=False if in production
- run `make build`
- run `make debug`

## Project Commands
- Build docker containers
  - `make build`
- Clean up extra python files
  - `make clean`
- Start debug server
  - `make debug`
- Serve flask app with gunicorn
  - `make serve`
- Start an interactive shell
  - `make shell`
- Stop **plog** container
  - `make stop`
- Run black code formatter
  - `make black`



