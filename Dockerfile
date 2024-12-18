FROM python:3.12-alpine

RUN apt-get update && apt-get install -y gcc \
    libpq-dev \
    curl \
    wget \
    ca-certificates \
    gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
    --output-document db_root.crt && \
    chmod 0600 db_root.crt

COPY requirements/prod.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY pastehub /app/

ENV GUNICORN_WORKERS=3

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]