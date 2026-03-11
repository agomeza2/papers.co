FROM python:3.11-slim

WORKDIR /engine

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY indexer.py .

CMD ["python", "indexer.py"]
