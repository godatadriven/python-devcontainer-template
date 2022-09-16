FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

RUN pip install --upgrade pip

# Install pip dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt