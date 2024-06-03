PROJECT := message-manager-api
.DEFAULT_GOAL := docker-up

docker-build:
	@docker build \
		-t message-manager-api \
		--build-arg PACKAGE_NAME=message-manager-api \
		--build-arg BUILD_REF=`git rev-parse --short HEAD` \
		--build-arg BUILD_DATE=`date -u +”%Y-%m-%dT%H:%M:%SZ”` \
		.
		
message-manager-api: 
	@go run ./cmd/api/main.go

docker-up:
	@docker-compose up --build --remove-orphans

docker-down:
	@docker-compose down

migrate-up:
	@alembic -c /usr/src/message-manager-api/migrations/alembic.ini upgrade head

migrate-down:
	@alembic -c /usr/src/message-manager-api/migrations/alembic.ini downgrade base