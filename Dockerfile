# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Create a virtual environment to avoid conflicts
RUN python -m venv /opt/venv

# Set the virtual environment path
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies in the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
COPY . .

# Set the start command for the app
CMD ["python", "app.py"]
