FROM python:3.12-slim

RUN apt-get update -y && \
    apt-get install -y build-essential libpq-dev libpq5 postgresql-client && \
    apt-get clean

WORKDIR /shopping-cart

COPY . /shopping-cart

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
