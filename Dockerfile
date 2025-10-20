# Use a base image with a smaller footprint (Debian slim)
FROM debian:bullseye-slim

# Install Python 3.9 and other necessary dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-distutils \
    python3.9-venv \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set python3.9 as the default python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Install pip for Python 3.9
RUN curl https://bootstrap.pypa.io/get-pip.py | python3

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies in Python 3.9
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
COPY . .

# Set the start command for the app
CMD ["python3", "app.py"]
