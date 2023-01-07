.PHONY: test

test:
	PYTHONPATH=./app pytest

.PHONY: serve

serve:
	uvicorn app.main:app --reload
