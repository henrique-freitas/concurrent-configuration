.PHONY: build run test

build:
	docker build -t config-validator .

run:
	docker run --rm -v $(PWD)/examples:/app/examples config-validator --path /app/examples

test:
	pytest -v