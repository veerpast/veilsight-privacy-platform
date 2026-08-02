.PHONY: setup setup-full api web demo test

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r backend/requirements.txt
	cd frontend && npm install

setup-full: setup
	.venv/bin/pip install -r backend/requirements-full.txt

api:
	PYTHONPATH=backend .venv/bin/uvicorn app.main:app --reload --port 8000

web:
	cd frontend && npm run dev

demo:
	./scripts/start_demo.sh

test:
	PYTHONPATH=backend python3 -m unittest discover -s backend/tests -v
	cd frontend && npm run build
