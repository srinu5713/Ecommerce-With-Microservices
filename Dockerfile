# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /user_management

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .

# Copy template files
COPY templates/a_home.html templates/
COPY templates/u_home.html templates/
COPY templates/login.html templates/
COPY templates/signup.html templates/
COPY templates/profile.html templates/

# Copy static files
COPY static/logo.png static/
COPY static/styles.css static/

ENV FLASK_APP=app.py

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
