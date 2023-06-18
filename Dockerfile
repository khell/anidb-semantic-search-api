FROM python:3.10-slim AS builder
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
RUN apt-get update
# For healthcheck
RUN apt-get -y install curl
WORKDIR /app
COPY LICENSE .
COPY anidb_query_tool.py .
COPY logger.py .
COPY main.py .
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8080
HEALTHCHECK --start-period=600s --retries=999 CMD curl --fail http://localhost:8080/healthcheck || exit 1
CMD ["gunicorn", "main:app", "--workers", "1", "--timeout", "60", "--bind", "0.0.0.0:8080"]
