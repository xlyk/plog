#!/bin/bash

GREEN="\033[1;32m"
NC="\033[0m"
LINES="========================================\n"

if [ "$DEBUG" == true ]
then
  # debug is enabled
  printf "\n${GREEN}${LINES}django - debug mode enabled\n${LINES}${NC}\n"
  pipenv run -- ./manage.py migrate
  printf "\n"
  pipenv run -- ./manage.py runserver 0.0.0.0:3333
  exit
fi

# continue with production settings
pipenv run -- ./manage.py migrate
printf "${GREEN}starting gunicorn on port 3333${NC}\n"
pipenv run  -- gunicorn core.wsgi:application -b 0.0.0.0:3333 --access-logfile /logs/gunicorn-access.log --error-logfile /logs/gunicorn-error.log
