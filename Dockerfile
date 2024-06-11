FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get clean

WORKDIR /usr/src/app

COPY . /usr/src/app/

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "bot/bot.py"]