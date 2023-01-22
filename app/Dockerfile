FROM python:latest

RUN apt-get update -y && \
  apt-get install -y python3-pip python3-dev

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "./app.py"]