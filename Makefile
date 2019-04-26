.PHONY: black build shell debug serve

NAME=plog
TAG=plog:latest
PORT=8000
WORKERS=4

black:
	@ # run black code formatter (https://github.com/ambv/black)
	black .

build:
	@ # build docker container
	docker build -t ${TAG} .

shell:
	@ # start an interactive shell
	${MAKE} build
	docker run --rm -it --name ${NAME}_shell \
		-v $(shell pwd):/app --env-file=.env ${TAG} /bin/sh

debug:
	@ # start debug server
	${MAKE} build
	docker run --rm -it \
		--name ${NAME} \
		-p ${PORT}:${PORT} \
		-v $(shell pwd):/app \
		--env-file=.env \
		${TAG}

serve:
	@ # serve flask app with gunicorn
	${MAKE} build
	docker run --rm -d \
		--name ${NAME} \
		-p ${PORT}:${PORT} \
		--env-file=.env \
		${TAG} \
		gunicorn -w ${WORKERS} -b 0.0.0.0:${PORT} main:app

stop:
	@ # stop plog container
	docker rm -fv plog
