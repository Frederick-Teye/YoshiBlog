FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ARG COLLECTSTATIC=0
RUN if [ "$COLLECTSTATIC" = "1" ]; then python manage.py collectstatic --noinput; fi

EXPOSE 8000
CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]