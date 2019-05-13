build:
	@docker-compose --project-directory ./ -f docker/docker-compose.yaml build --no-cache
run: build
	@docker-compose --project-directory ./ -f docker/docker-compose.yaml up -d
sh:
	@docker exec -it ssp /bin/sh
log:
	@docker logs -tf ssp
upgrade:
	@docker exec -it ssp flask db upgrade
typing-check:
	@docker exec -it ssp mypy src/ --ignore-missing-imports
syntax-check:
	@docker exec -it ssp flake8
tests:
	@docker exec -it ssp pytest
stop:
	@docker-compose --project-directory ./ -f docker/docker-compose.yaml stop
clean: stop
	@docker-compose --project-directory ./ -f docker/docker-compose.yaml rm -vf ssp ssp_database
clean-dangling-images: clean
	@docker rmi -f $(docker images -q --filter "dangling=true")

.PHONY: build run sh log upgrade typing-check syntax-check tests stop clean clean-dangling-images
