FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HEARTLIGHT_DATA_ROOT=/data

WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir '.[server]'

RUN useradd --create-home --uid 10001 heartlight \
    && mkdir -p /data \
    && chown -R heartlight:heartlight /data /app
USER heartlight

EXPOSE 8080
CMD ["uvicorn", "heartlight.api:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
