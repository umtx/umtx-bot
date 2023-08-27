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
# RUN apt-get install -y \
#     fonts-liberation \
#     libasound2 \
#     libatk-bridge2.0-0 \
#     libatk1.0-0 \
#     libatspi2.0-0 \
#     libcups2 \
#     libdbus-1-3 \
#     libdrm2 \
#     libgbm1 \
#     libgtk-3-0 \
# #    libgtk-4-1 \
#     libnspr4 \
#     libnss3 \
#     libwayland-client0 \
#     libxcomposite1 \
#     libxdamage1 \
#     libxfixes3 \
#     libxkbcommon0 \
#     libxrandr2 \
#     xdg-utils \
#     libu2f-udev \
#     libvulkan1

# # Update and install necessary packages

# # Install Google Chrome

# RUN curl -LO  https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb
# RUN apt-get install -y ./google-chrome-stable_114.0.5735.90-1_amd64.deb

# # RUN sleep 6000;cqlsh -f build_all.cql
# RUN rm google-chrome-stable_114.0.5735.90-1_amd64.deb

# RUN echo "Chrome: " && google-chrome --version


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

# Set the working directory
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install project dependencies using Poetry
RUN poetry install

# Start your application (replace with your actual command)
CMD ["sh", "run.sh"]
