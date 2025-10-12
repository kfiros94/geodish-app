# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
RUN pip install gunicorn

# Copy application code
COPY app/ ./app/
COPY static/ ./static/

# Update PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.app:app"]
