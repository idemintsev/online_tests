FROM python:3.8.10
RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN ls .

COPY . .

EXPOSE 8000