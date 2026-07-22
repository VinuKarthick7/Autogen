FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn websockets redis pydantic

COPY . .

ENV PYTHONPATH=/app
ENV REDIS_URL=redis://redis:6379

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
