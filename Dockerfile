# Use a minimal Python image
FROM python:3.9-slim

# Install pip
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port for Render
EXPOSE 10000

# Command to run the app
CMD ["python3", "app.py"]
