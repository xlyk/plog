.PHONY: black build shell debug serve

black:
	@ # run black code formatter (https://github.com/ambv/black)
	black .

build:
	@ # build docker container
	docker-compose build

clean:
	@ # clean up extra python files
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

debug:
	@ # start debug server
	docker-compose run --rm --service-ports -e IS_DEBUG=true plog

serve:
	@ # serve flask app with gunicorn
	docker-compose up -d

shell:
	@ # start an interactive shell
	docker-compose run --rm --service-ports plog sh

stop:
	@ # stop plog container
	docker-compose rm -sfv plog

