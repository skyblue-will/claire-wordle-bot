FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

# Create data directory
RUN mkdir -p /app/data

ENV DATA_DIR=/app/data

CMD ["python", "bot.py"]
