.PHONY: test

test:
	docker-compose up -d && docker-compose run web test
