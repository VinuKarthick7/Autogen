FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install streamlit websockets

COPY . .

ENV PYTHONPATH=/app
ENV API_URL=http://api:8000

CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
