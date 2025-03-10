FROM python:3.12.9-bullseye AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

### Debugger
FROM base AS debug

RUN pip install debugpy

EXPOSE 8000
EXPOSE 5678

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "manage.py", "runserver", "0.0.0.0:8000"]

### Main
FROM base AS main

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
