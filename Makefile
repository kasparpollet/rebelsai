#File used only during development

include .env
docker_compose = docker-compose -f devops/Dockercompose.yml
docker_web = docker exec -it rebelsai
docker_db_exec = docker exec -i rebelsai-postgres-db
docker_db = docker exec -it rebelsai-postgres-db

.PHONY: up
up: # Builds, (re)creates, starts, and attaches to containers for a service. Deletes all previously created contianer images
	@$(docker_compose) up -d --build; docker images -q |xargs docker rmi;

.PHONY: logs
logs: # View the logs of rebelsai activity
	@$(docker_compose) logs -f --tail=100

.PHONY: stop
stop: # Stop all containers
	@$(docker_compose) stop

.PHONY: down
down: # Stops containers and removes containers, networks, volumes, and images created by `make up`
	@$(docker_compose) down

.PHONY: shell
shell: # Enter the shell of the docker contianer where rebelsai is running
	@$(docker_web) sh -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec bash";

.PHONY: shell-db
shell-db: # Enter the shell of the docker where rebelsai is running
	@$(docker_db) sh -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec bash";

.PHONY: migrate
migrate: # Execute migrate command in rebelsai container
	@$(docker_web) python manage.py migrate

.PHONY: makemigrations
makemigrations: # Execute makemigrations command in rebelsai container
	@$(docker_web) python manage.py makemigrations

.PHONY: db-rebuild-migrations
db-rebuild-migrations:
	@$(docker_db_exec) psql -U rebelsai -d dbrebelsai < devops/db/drop_and_create_schema.sql
	@$(docker_db_exec) psql -U rebelsai -d dbrebelsai < database.bak

.PHONY: db-redeploy
db-redeploy: db-rebuild-migrations migrate

.PHONY: db-backup
db-backup: 
	@$(docker_db) pg_dump -U postgres dbrebelsai > db_backup.sql

.PHONY: install-requirements
install: # Execute migrate command in rebelsai container
	@$(docker_web) pip install -r /app/requirements.txt