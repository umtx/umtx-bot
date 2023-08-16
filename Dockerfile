# Use Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable
# RUN sleep 6000;cqlsh -f build_all.cql




# Install Python and pip
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip

# Install Poetry
RUN pip3 install poetry

# Set the working directory
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install project dependencies using Poetry
RUN poetry install

# Start your application (replace with your actual command)
CMD ["sh", "start.sh"]
