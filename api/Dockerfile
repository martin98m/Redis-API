FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask redis

EXPOSE 5000

CMD ["python", "server.py"]