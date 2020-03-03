.PHONY: build img

DOCKERFILE="django_base"

build:
	make -s img

img:
	docker build -t ${DOCKERFILE}:latest -f ${DOCKERFILE} .

start:
	docker run -it -v $(shell pwd)/file_share_app/:/var/www/ ${DOCKERFILE}
