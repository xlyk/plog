.PHONY: black build shell debug serve

TAG=plog:latest

# run black code formatter (https://github.com/ambv/black)
black:
	black .

# build docker container
build:
	docker build -t ${TAG} .

# start an interactive shell
shell:
	docker run --rm -it ${TAG} /bin/sh

# start debug server
debug:
	docker run --rm -it -p 8000:8000 ${TAG}

# serve flask app with gunicorn
serve:
	docker run --rm -d \
		--name plog \
		-p 8000:8000 \
		${TAG} gunicorn -w 4 -b 0.0.0.0:8000 main:app

