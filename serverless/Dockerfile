# Use the official Python base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy function code
COPY main.py .
COPY threads_downloader.py .
COPY ai_nsfw_detection.py .
COPY ai_captioning.py .
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Set the command to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
