# Use official Python slim image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir fastapi uvicorn pillow

# Expose port
EXPOSE 8000

# Environment variables for auth (default values)
ENV API_USERNAME=admin
ENV API_PASSWORD=mypassword

# Command to run the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
