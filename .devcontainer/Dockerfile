FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install Java
RUN sudo apt update && \
    sudo apt install default-jdk -y

# Upgrade pip
RUN pip install --upgrade pip

# Install pip dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Install Devcontainer dependencies
COPY .devcontainer/requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt && \
    rm /tmp/requirements-dev.txt