.PHONY: api worker dashboard benchmark up down

api:
	uvicorn main:app --reload

worker:
	python -m api.workers.executor

dashboard:
	streamlit run streamlit_app/app.py

benchmark:
	python -m api.workers.benchmark_executor

up:
	docker-compose up --build -d

down:
	docker-compose down
