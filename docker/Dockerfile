FROM python:3-slim AS base

WORKDIR /app

FROM base AS builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base AS app

RUN apt-get update
RUN apt-get install --no-install-recommends -y ffmpeg
RUN apt-get autoremove

ENV PATH="/opt/venv/bin:$PATH"

COPY docker/docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

COPY --from=builder /opt/venv /opt/venv
COPY *.py .

VOLUME [ "/data" ]

ENTRYPOINT [ "/bin/sh", "/docker-entrypoint.sh" ]
