.PHONY: api worker dashboard benchmark

api:
	uvicorn main:app --reload

worker:
	python -m api.workers.executor

dashboard:
	streamlit run streamlit_app/app.py

benchmark:
	python -m api.workers.benchmark_executor
