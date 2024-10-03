# Use the official Python image as a base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (like Chromium and other utilities)
RUN apt-get update && apt-get install -y \
    chromium \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY app.py .
COPY templates/ ./templates/

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/bin/chromium

# Set Chrome options to run in headless mode
ENV DISPLAY=:99

# Command to run your app
CMD ["python", "app.py"]
