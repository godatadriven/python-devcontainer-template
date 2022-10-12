FROM python:3.10

# Install Java
RUN apt update && \
    apt install -y sudo && \
    sudo apt install default-jdk -y

# Add non-root user
ARG USERNAME=nonroot
RUN groupadd --gid 1000 $USERNAME && \
    useradd --uid 1000 --gid 1000 -m $USERNAME
## Make sure to reflect new user in PATH
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

## Pip dependencies
USER $USERNAME
# Upgrade pip
RUN pip install --upgrade pip
# Install production dependencies
COPY --chown=nonroot:1000 requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
# Install development dependencies
COPY --chown=nonroot:1000 requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt && \
    rm /tmp/requirements-dev.txt


# Install ZSH
USER root
RUN apt update && \
    apt install -y zsh && \
    chsh -s $(which zsh)

# Install Oh My ZSH
USER $USERNAME
RUN wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O - | zsh || true && \
    cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc

# wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O - | sh -- -y
# USER $USERNAME


ENTRYPOINT ["/bin/zsh"]