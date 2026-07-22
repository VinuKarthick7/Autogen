FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install redis

COPY . .

ENV PYTHONPATH=/app
ENV REDIS_URL=redis://redis:6379

CMD ["python", "-m", "api.workers.executor"]
