FILE			= ./src/docker-compose.yml
DOCKER_CMD		= docker compose -f ${FILE}

DJANGO_CONTNR	= django
POSTGRES_CONTNR	= database

DJANGO_IMAGE	= django:custom
POSTGRES_IMAGE	= database:custom

NETWORK		= bedb
VOLUME_DIR	= ./src/data
DB_VOLUME	= dev-db-data

all: build up

build:
	${DOCKER_CMD} build

up:
	${DOCKER_CMD} up -d 

down:
	${DOCKER_CMD} down

create_data_folder:
	mkdir -p ${VOLUME_DIR}

goin_django:
	docker exec -it ${DJANGO_CONTNR} /bin/bash

goin_postgres:
	docker exec -it ${POSTGRES_CONTNR} /bin/bash


test:
	${DOCKER_CMD} build
	${DOCKER_CMD} up -d 
	${DOCKER_CMD} exec ${DJANGO_CONTNR} pwd
	${DOCKER_CMD} exec ${DJANGO_CONTNR} ls -R /app
	${DOCKER_CMD} exec ${DJANGO_CONTNR} python app/src/django/app/manage.py test --settings=bookoverflow.test_settings


clean: rm_containers rm_images rm_volumes rm_networks rm_migration_files prune

full_clean: clean rm_data

prune:
	docker system prune

rm_containers:
	docker rm -f ${DJANGO_CONTNR} ${POSTGRES_CONTNR}

rm_images:
	docker rmi -f ${DJANGO_IMAGE} ${POSTGRES_IMAGE}

rm_volumes:
	docker volume rm -f ${DB_VOLUME}

rm_networks:
	if docker network inspect ${NETWORK} > /dev/null; then \
		docker network rm ${NETWORK}; \
	fi

rm_data:
	sudo rm -rf ${VOLUME_DIR}

rm_migration_files:
	sudo find ./src/django/ -name '0*_initial.py' -type f -delete

re: clean all