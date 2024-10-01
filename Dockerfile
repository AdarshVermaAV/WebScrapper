# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install required packages for Chrome
RUN apt-get update && apt-get install -y \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy specific application files into the container
COPY app.py .
COPY templates/ ./templates/  # Copy the entire templates directory

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV DISPLAY=:99

# Specify the command to run your app
CMD ["python", "app.py"]

# Expose the port on which your app runs
EXPOSE 5000
