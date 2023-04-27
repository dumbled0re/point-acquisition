docker_build_local:
	docker-compose -f docker/docker-compose-local.yml up -d --build

docker_build:
	docker-compose -f docker/docker-compose.yml up -d --build

docker_up_local:
	docker-compose -f docker/docker-compose-local.yml up -d

docker_up:
	docker-compose -f docker/docker-compose.yml up -d

docker_down_local:
	docker-compose -f docker/docker-compose-local.yml down

docker_down:
	docker-compose -f docker/docker-compose.yml down

exec_main:
	docker exec app python main.py

exec_auto_deposit_autoracing:
	docker exec app python ./auto_deposit_rakuten_horse_racing/auto_deposit_autoracing.py
