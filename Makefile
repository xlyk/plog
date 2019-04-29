.PHONY: black build shell debug serve

black:
	@ # run black code formatter (https://github.com/ambv/black)
	black .

build:
	@ # build docker container
	docker-compose build

shell:
	@ # start an interactive shell
	docker-compose run --rm --service-ports plog sh

debug:
	@ # start debug server
	docker-compose run --rm --service-ports plog sh start_gunicorn.sh

serve:
	@ # serve flask app with gunicorn
	docker-compose up -d

stop:
	@ # stop plog container
	docker-compose rm -sfv plog

