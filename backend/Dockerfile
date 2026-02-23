FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY ./backend /app
# Copy frontend into a static folder that can be served by nginx or Flask
COPY ./frontend /app/frontend

# Install python deps
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV SERVE_FRONTEND=true

EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:5000", "--workers", "4", "--threads", "4", "--log-level", "info"]
