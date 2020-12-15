## all: install-devenv
# install-devenv: build

# Build the docker container
build:
	docker-compose pull
	docker-compose build

stack-up:
	docker-compose up -d

# Clean up docker container
stack-purge:
	docker-compose stop
	docker-compose kill
	docker-compose rm

# Refresh dependencies (Docker images) and rebuild
stack-full-refresh:
	docker-compose build --no-cache --pull

# Enter 'dev' container with bash
dev-bash:
	docker-compose run --rm --entrypoint "/bin/bash -c" gdelt_docker bash

# make hello name=Worlid
hello:
	docker-compose run --rm gdelt_docker python3 app/commands/test.py batch hello 

# make run-main
run-main:
	docker-compose run --rm gdelt_docker python3 gdelt_code/main.py batch main
