docker_build_local:
	docker-compose -f docker/docker-compose-local.yml up -d --build

docker_build_splash:
	docker-compose -f docker/docker-compose-splash.yml up -d --build

docker_build:
	docker-compose -f docker/docker-compose.yml up -d --build

docker_up_local:
	docker-compose -f docker/docker-compose-local.yml up -d

docker_up_splash:
	docker-compose -f docker/docker-compose-splash.yml up -d

docker_up:
	docker-compose -f docker/docker-compose.yml up -d

docker_down_local:
	docker-compose -f docker/docker-compose-local.yml down

docker_down_splash:
	docker-compose -f docker/docker-compose-splash.yml down

docker_down:
	docker-compose -f docker/docker-compose.yml down

exec_test:
	docker exec local_app python test.py $(TARGET)

exec_auto_deposit_autoracing:
	docker exec app python ./auto_deposit_autoracing.py

exec_auto_get_point_income:
	docker exec app python ./auto_get_point_income.py

exec_auto_deposit_spat4:
	docker exec app python ./auto_deposit_spat4.py

exec_auto_get_point_income_local:
	docker exec local_app python ./auto_get_point_income_local.py