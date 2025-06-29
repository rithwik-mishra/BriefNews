# Development stage
FROM python:3.11-slim

# Install Node.js 20 and npm with security updates
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    curl \
    git \
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && node --version \
    && npm --version \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Angular CLI globally
RUN npm install -g @angular/cli

# Create vscode user
RUN useradd -ms /bin/bash vscode

# Set working directory
WORKDIR /app

# Copy requirements file first for better caching
COPY requirements.txt .

# Install Python dependencies with security updates
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy package files for frontend
COPY frontend/package*.json frontend/

# Install frontend dependencies
RUN cd frontend && npm install

# Copy the rest of the application
COPY . .

# Set permissions
RUN chown -R vscode:vscode /app

# Switch to vscode user
USER vscode

# Expose ports for Angular and FastAPI
EXPOSE 4200 8000

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command for development
CMD ["sh", "-c", "echo 'Dev container ready. Use the terminal to start your services.'"] 