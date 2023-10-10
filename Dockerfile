# Use Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# RUN sleep 6000;cqlsh -f build_all.cql
RUN  sed -i 's|http://archive.|http://vn.archive.|g' /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y \
    curl \
    gnupg \
    wget 



RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Install Poetry
RUN apt-get install -y wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.11 python3-pip
RUN pip3 install poetry



# Install Python and pip
RUN apt-get update && \
    apt-get install -y \
    python3-pip
RUN apt-get install -y openssh-server


# Set the working directory
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install project dependencies using Poetry
RUN poetry install

# Start your application (replace with your actual command)
CMD ["sh", "run.sh"]
