# Dockerfile
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
#COPY . .

# Change ownership so non-root user can access
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose FastAPI port
EXPOSE 8009

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8009", "--workers", "4"]
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8009", "--workers", "4", "--timeout", "300"]
