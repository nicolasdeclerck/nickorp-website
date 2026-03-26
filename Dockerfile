FROM node:20-slim AS tailwind
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY static/ ./static/
COPY templates/ ./templates/
RUN npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=tailwind /app/static/css/output.css ./static/css/output.css

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["gunicorn", "nickorp.wsgi:application", "--bind", "0.0.0.0:8000"]
