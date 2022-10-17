# How to create a Devcontainer for your Python project 🐳

<!-- Docker has been around for a while now, revolutionizing the way we think about packaging and deploying software. But there are still more opportunities in store for us. Whereas it was already possible to streamline the CI/CD with the production environment by reusing the same image bases, the development environment often still diverged. And this is where Devcontainers can offer a solution. By connecting your IDE to the same container used in production, we can be sure our environment is aligned across all places.

Devcontainers have seen massive developments and adoption over the past years. VSCode provides support for using Devcontainers and GitHub has been pushing their Codespaces: their completely managed remote Devcontainer service. Are you excited yet? Let's dive in. -->

## The challenge: onboarding newcomers & mismatched environments

> 📢 Everything discussed is accessible in the [godatadriven/python-devcontainer-template](https://github.com/godatadriven/python-devcontainer-template) repo

Take the following scenario. Your company uses Apache Spark to process data, and your team has pyspark set up in a Python project. The codebase is built on a specific Python version, using a certain Java installation, and an accompanying pyspark version that works with the former. To onboard a new member, you will need to pass a list of instructions the developer needs to follow carefully in order to get their setup working. But not everyone might run this on the same laptop environment: different hardware, different operating systems. This is getting challenging.

But the setup is a one-off, right? Just go through the setup once and you’ll be good. Not entirely. Your code environment will change over time: your team will probably install, update or remove packages during the project’s development. This means that if a developer creates a new feature and changes its own environment to do so; it also needs to make sure that the other team members change theirs and that the production environment is updated accordingly. This makes it easy to get mis-aligned environments: between developers, between development and production.

We can do better than this! Instead of giving other developers a setup document, let’s make sure we also create formal instructions so we can *automatically* set up the development environment. Docker lets us do exactly this – on which Devcontainers are built on top of. 
<!-- ~~Devcontainers to the rescue ⛑~~.  -->
Devcontainers can help us:

- ⚡️ Instantly onboard new team members onto your project
- 🔄 Get a reproducible development environment
- 👨‍👩‍👧‍👦 Better align the environments between team members
- ⏱ Keeping your dev environment up-to-date & reproducible saves you team going into production later

Let’s explore how we can set up a Devcontainer for your Python project!

## Creating your first Devcontainer

<!-- > Step 1 -->
> 

> This tutorial is focused on **VSCode**. Other IDE’s like PyCharm support running in Docker containers but support is less comprehensive than on VSCode.
> 

### 📌 Recap

To recap, we are trying to create a dev environment that installs the following:

- Python
- Pyspark
- Java

And we want to do so *automatically*, that is, inside a Docker image.

### Project structure

Let’s say we have a really simple project that looks like this:

```bash
$ tree .
.
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── sales_analysis.py
└── test_sales_analysis.py
```

That is, we have a Python module with an accompanying test, a `requirements.txt` file describing our production dependencies (pyspark) and a `requirements-dev.txt` describing dependencies that should be installed in development only (pytest, black, mypy). Now let’s see how we can extend this setup to include a Devcontainer.

### The `.devcontainer` folder

Your Devcontainer spec will live inside the `.devcontainer` folder. There will be two main files:

- `devcontainer.json`
- `Dockerfile`

Create a new file called `devcontainer.json`:

`.devcontainer/devcontainer.json`:

```json
{
    "build": {
        "dockerfile": "Dockerfile",
        "context": ".."
    }
}
```

This does basically means: as a base for our Devcontainer, use the `Dockerfile` located in the current directory, and build it with a *current working directory* (cwd) of `..`.

So how does this `Dockerfile` look like?

`.devcontainer/Dockerfile`:

```docker
FROM python:3.10

# Install Java
RUN apt update && \
    apt install -y sudo && \
    sudo apt install default-jdk -y

# Upgrade pip
RUN pip install --upgrade pip

# Install pip dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Install Devcontainer dependencies
COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt && \
    rm /tmp/requirements-dev.txt
```

We are building our image on top of `python:3.10`, which is a Debian-based image. This is one of the Linux distributions that a Devcontainer can be built on. The main requirement is that Node.js should be able to run: VSCode automatically installs VSCode Server on the machine. For an extensive list of supported distributions, see [“Remote Development with Linux”](https://code.visualstudio.com/docs/remote/linux).

On top of `python:3.10`, we install Java and the required pip packages.

### Opening the Devcontainer

The `.devcontainer` folder in place, now it’s time to open our Devcontainer.

First, make sure you have the Dev Containers extension installed in VSCode (previously called “Remote - Containers”:

[Install Dev Containers VSCode Extension](vscode:extension/ms-vscode-remote.remote-containers)

[Dev Containers - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

If you open your repo again, the extension should already detect your Devcontainer:

![folder contains a dev container config file](https://godatadriven.com/wp-content/uploads/2022/10/folder-contains-a-dev-container-config-file.png)

Alternatively, you can open up the command pallete (<kbd>CMD</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) and select “*Dev Containers: Reopen in Container*”:

![Dev Containers: Reopen in Container](https://godatadriven.com/wp-content/uploads/2022/10/reopen-in-devcontainer-notification.png)

Your VSCode is now connected to the Docker container 🙌🏻:

![VSCode is now connected to the Docker container](https://godatadriven.com/wp-content/uploads/2022/10/opening-the-devcontainer.gif)

### What is happening under the hood 🚗

Besides starting the Docker image and attaching the terminal to it, VSCode is doing a couple more things:

1. [**VSCode Server**](https://code.visualstudio.com/docs/remote/vscode-server) is being installed on your Devcontainer. VSCode Server is installed as a service in the container itself so your VSCode installation can communicate with the container. For example, install and run extensions.
2. **Config is copied** over**.** Config like `~/.gitconfig` and `~/.ssh/known_hosts` are copied over to their respective locations in the container.
This then allows you to use your Git repo like you would do normally, without re-authenticating.
3. **Filesystem mounts**. VSCode automatically takes care of mounting: 1) The folder you are running the Devcontainer from and 2) your VSCode workspace folder.

## Extending the Devcontainer

We have built a working Devcontainer, that is great! But a couple things are still missing.

### Installing a non-root user

<!-- > Step 2 -->

If you `pip install` a new package, you will see the following message:

![The warning message: “*WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: [https://pip.pypa.io/warnings/venv](https://pip.pypa.io/warnings/venv)*](https://godatadriven.com/wp-content/uploads/2022/10/running-pip-as-root.png)

> Running your application as a non-root user is recommended even in production (since it is more secure), so this is a good idea even if you're reusing an existing Dockerfile.
— [Add non-root user | VSCode Docs](https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user)

<!-- This is because we are connecting to the container as the `root` user. This is not a good practice, so let’s fix this. We can add a non-root user by running:

```bash
sudo adduser my_custom_non_root_user
``` -->

```bash
# Add non-root user
ARG USERNAME=nonroot
RUN groupadd --gid 1000 $USERNAME && \
    useradd --uid 1000 --gid 1000 -m $USERNAME
## Make sure to reflect new user in PATH
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
USER $USERNAME
```

Add the following property to `devcontainer.json`:

```json
    "remoteUser": "nonroot"
```

### ~~Installing ZSH~~

→ Put in **Gist** and share in extra resources.

```bash
# Install ZSH
USER root
RUN apt update && \
    apt install -y zsh && \
    chsh -s $(which zsh)

# Install Oh My ZSH
USER $USERNAME
RUN wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O - | zsh || true && \
    cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc

ENTRYPOINT ["/bin/zsh"]
```

```json

```

### Passing custom VSCode settings

<!-- > Step 3 -->

<excalidraw drawing of overriding settings>

Our Devcontainer is still a bit bland, without extensions and settings. Besides any custom extensions a user might want to install, we can install some for them by default already. We can define such settings in `customizations.vscode`:

```json
     "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python"
            ],
            "settings": {
                "python.testing.pytestArgs": [
                    "."
                ],
                "python.testing.unittestEnabled": false,
                "python.testing.pytestEnabled": true,
                "python.formatting.provider": "black",
                "python.linting.mypyEnabled": true,
                "python.linting.enabled": true
            }
        }
    }
```

The defined extensions are always installed in the Devcontainer. However, the defined settings provide just a **default** for the user to use, and can still be overriden by other setting scopes like: User Settings, Remote Settings or Workspace Settings.

### Accessing Spark UI

<!-- > Step 4 -->

Since we are using pyspark, it would be nice to be able to access **Spark UI**. When we start a Spark session, VSCode will ask whether you want to forward the specific port. Since we already know this is Spark UI, we can do so automatically:

```json
    "portsAttributes": {
        "4040": {
            "label": "SparkUI",
            "onAutoForward": "notify"
        }
    },

    "forwardPorts": [
        4040
    ]
```

When we now run our code, we get a notification we can open Spark UI in the browser:

![open Spark UI in the browser](https://godatadriven.com/wp-content/uploads/2022/10/application-running-on-port-4040.png)

## Running our CI in the Devcontainer

<!-- > Step 5 -->
> 

2 options:

1. ~~Build image periodically, then use in QA step~~

2. ~~Build image as part of QA step~~

1. Using `devcontainers/ci`
2. Prebuilding the image

[comment]: <> (Include a nice image of building and then using the image in CI)

### Using `devcontainers/ci`

https://github.com/devcontainers/ci

```yaml
name: Python app

on:
  pull_request:
  push:
    branches:
      - "**"

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout (GitHub)
        uses: actions/checkout@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.repository_owner }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and run dev container task
        uses: devcontainers/ci@v0.2
        with:
          imageName: ghcr.io/${{ github.repository }}/devcontainer
          runCmd: pytest .
```

![running-ci-in-the-devcontainer-github-actions](https://godatadriven.com/wp-content/uploads/2022/10/running-ci-in-the-devcontainer-github-actions.png)

### Pre-building the image

```yaml
name: Build image

on:
  push:
    branches:
      - "main"
    paths:
      - '.devcontainer/**'
      - 'requirements.txt'

jobs:
  build_image:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout (GitHub)
        uses: actions/checkout@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.repository_owner }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and run dev container task
        uses: devcontainers/ci@v0.2
        with:
          imageName: ghcr.io/${{ github.repository }}/devcontainer
          runCmd: echo "Success"
```

```json
{
    "build": {
        "cacheFrom": "ghcr.io/godatadriven/python-devcontainer-template/devcontainer"
    }
}
```

## Devcontainer architecture: Three environments 🎁

With the CI now set up, we can see we basically have 3 environments:

![three-environments-docker-images-devcontainer](https://godatadriven.com/wp-content/uploads/2022/10/three-environments-docker-images-devcontainer-setup.png)

## Going further 🔮
There's lots of other resources to explore; Devcontainers are well-documented and there are many posts about it. If you're up for more, let's see what else you can do.
### Using Devcontainer features

Devcontainer [features](https://containers.dev/features) allow you to easily extend your Docker definition with common additions.

<!-- ~~Then, you will have to go through all the CLI steps. Fortunately, though, there is a Devcontainer ‘*feature*’ that does installs a non-root user for us.~~

[~~https://github.com/devcontainers/features/tree/main/src/common-utils~~](https://github.com/devcontainers/features/tree/main/src/common-utils) -->

<aside>
💡 ~~Be advised, the above specifications are brand-new (as of writing, October 2022), and can be prone to change.~~

</aside>

### Using one of Microsoft’s base images

→ explain we can better use `[mcr.microsoft.com/vscode/devcontainers/python](http://mcr.microsoft.com/vscode/devcontainers/python):3.10` instead of `python:3.10`

### Mounting directories

- AWS credentials
- Azure credentials
- GCP credentials

### Docker compose

### Awesome resources

- https://github.com/manekinekko/awesome-devcontainers
- https://github.com/devcontainers/ci
- https://github.com/devcontainers/cli
- https://containers.dev/
- [https://github.com/devcontainers/images](https://github.com/devcontainers/images)

## Concluding

## About

This blogpost is written by Jeroen Overschie, working at GoDataDriven.

---

GoDataDriven is a specialist in Data and AI, providing high-quality consultancy services for clients in The Netherlands and beyond. Do you feel right at home in the Data & AI space and are you interested? Look at our [Hiring](https://godatadriven.com/careers/) page.

---

Inspiration

[Microsoft’s devcontainer.json: Just for VS Code or an evolving standard? •](https://www.notion.so/Microsoft-s-devcontainer-json-Just-for-VS-Code-or-an-evolving-standard-d7a4846882d040429c5088c719b36d91)