app_port = 8080

run:
	docker-compose -f ./docker-compose.dev.yaml up -d
	docker run -p ${app_port}:${app_port} --env-file ./.env 'translator-space'

build: env_file
	docker build --tag 'translator-space' .

env_file:
ifeq (,$(wildcard ./.env))
	@echo "Creating .env file from .env.example..."
	cp ./.env.example ./.env
endif

clean:
	docker stop $(shell docker ps -q --filter ancestor=translator-space ) 2>/dev/null || true
	docker rm $(shell docker ps -a -q --filter "ancestor=translator-space") 2>/dev/null || true
	docker-compose -f ./docker-compose.dev.yaml down --remove-orphans

rebuild: clean build