# Use Debian slim image as a base
FROM debian:bullseye-slim

# Install Python 3.9 and essential build tools
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-distutils \
    python3.9-venv \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.9 as the default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Install pip for Python 3.9
RUN curl https://bootstrap.pypa.io/get-pip.py | python3

# Set working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Use python3 to run the app
CMD ["python3", "app.py"]
