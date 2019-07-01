all: run

build_images:
	rm -rf var/dev/python \
 && mkdir -p var/dev/python \
 && docker-compose build

build_images_force:
	rm -rf var/dev/python \
 && mkdir -p var/dev/python \
 && docker-compose pull \
 && docker-compose build --force-rm --no-cache

run:
	mkdir -p var/dev/postgres_data \
 && mkdir -p var/dev/redis_data && chmod 777 var/dev/redis_data \
 && mkdir -p var/dev/python \
 && docker-compose up

refresh:
	mkdir -p var/dev/postgres_data \
 && mkdir -p var/dev/redis_data && chmod 777 var/dev/redis_data \
 && mkdir -p var/dev/python \
 && docker-compose run --rm backend bash ./deploy/install_requirements_dev.sh \
 && docker-compose run --rm backend python src/manage.py migrate --noinput \
 && docker-compose run --rm backend python src/manage.py clear_cache

test:
	mkdir -p var/dev/postgres_data \
 && mkdir -p var/dev/redis_data && chmod 777 var/dev/redis_data \
 && mkdir -p var/dev/python \
 && docker-compose run --rm backend python src/manage.py test --settings=core.test_settings src/

stop:
	docker-compose stop

shell:
	mkdir -p var/dev/postgres_data \
 && mkdir -p var/dev/redis_data && chmod 777 var/dev/redis_data \
 && mkdir -p var/dev/python \
 && docker-compose run --rm backend bash

clean:
	docker image prune -af

remove:
	docker-compose rm
