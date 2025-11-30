.PHONY: install run test clean

install:
	poetry install

run:
	poetry run uvicorn api.main:app --reload

test:
	poetry run pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
