# Use Python 3.9 as base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all the app files
COPY . .

# Set the start command
CMD ["python", "app.py"]
