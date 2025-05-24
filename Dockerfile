# Build stage for Angular
FROM node:20-slim AS angular-build
WORKDIR /app/frontend

# Install build dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy package files first to leverage Docker cache
COPY frontend/package*.json ./
RUN npm install --verbose

# Copy the rest of the frontend code
COPY frontend/ .
RUN npm run build --verbose

# Build stage for Python dependencies
FROM python:3.10-slim AS python-build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.10-slim

# Install Node.js for production
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Create vscode user
RUN useradd -ms /bin/bash vscode

# Set working directory
WORKDIR /app

# Copy built Angular app
COPY --from=angular-build /app/frontend/dist/frontend /app/frontend/dist

# Copy Python dependencies
COPY --from=python-build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=python-build /usr/local/bin /usr/local/bin

# Copy application code
COPY backend/ /app/backend/

# Create default .env file if it doesn't exist
RUN echo "PYTHONPATH=/app\nPYTHONUNBUFFERED=1" > /app/.env

# Set permissions
RUN chown -R vscode:vscode /app

# Switch to vscode user
USER vscode

# Expose ports
EXPOSE 8000

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run the production server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"] 