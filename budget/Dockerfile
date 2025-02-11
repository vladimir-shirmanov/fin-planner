FROM python:3.12-slim as builder
RUN apt-get -y update && \
apt-get -y install --no-install-recommends curl && \
apt-get clean && \
rm -rf /var/lib/apt/lists/* && \
pip install uv

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN uv pip install --system --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app
COPY ./.env /code/.env
EXPOSE 8083
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8083/health || exit 1

ENV PYTHONPATH=/code
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8083" ]