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

RUN curl -LO  https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb
RUN apt-get install -y ./google-chrome-stable_114.0.5735.90-1_amd64.deb

# RUN sleep 6000;cqlsh -f build_all.cql
RUN rm google-chrome-stable_114.0.5735.90-1_amd64.deb

RUN echo "Chrome: " && google-chrome --version




# Install Poetry
RUN apt install -y wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.11 python3-pip
RUN pip3 install poetry



# Install Python and pip
RUN apt-get update && \
    apt-get install -y \
    python3-pip

# Set the working directory
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install project dependencies using Poetry
RUN poetry install

# Start your application (replace with your actual command)
CMD ["sh", "run.sh"]
