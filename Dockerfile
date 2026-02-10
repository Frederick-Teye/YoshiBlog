FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=120 --retries=10 -r requirements.txt

COPY . .
ARG COLLECTSTATIC=0
RUN if [ "$COLLECTSTATIC" = "1" ]; then python manage.py collectstatic --noinput; fi

ENV AWS_LWA_PORT=8000
ENV AWS_LWA_READINESS_CHECK_PATH=/
ENV AWS_LWA_ASYNC_INIT=true

# Make the script executable
RUN chmod +x run.sh

EXPOSE 8000

# Change the CMD to execute our script
CMD ["./run.sh"]