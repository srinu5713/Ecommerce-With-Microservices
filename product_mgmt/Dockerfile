# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /product_management

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .

COPY templates ./templates
COPY static ./static

ENV FLASK_APP=app.py

# Expose the port the app runs on
# EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
