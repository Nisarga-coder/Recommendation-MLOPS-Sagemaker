# Use an official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local application files into the container
COPY . /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt 
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for AWS SageMaker endpoint
ENV AWS_REGION=us-west-2 \
    MODEL_ENDPOINT=your-sagemaker-endpoint

# Expose the port the app will run on
EXPOSE 8080

# Command to run the application with Gunicorn
# Includes:
# - Binding to 0.0.0.0:8080
# - Using 4 worker processes
# - Enabling worker thread concurrency
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--threads", "2", "app:app"]
