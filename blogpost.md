# How to create a Devcontainer for your Python project 🐳

<!-- Docker has been around for a while now, revolutionizing the way we think about packaging and deploying software. But there are still more opportunities in store for us. Whereas it was already possible to streamline the CI/CD with the production environment by reusing the same image bases, the development environment often still diverged. And this is where Devcontainers can offer a solution. By connecting your IDE to the same container used in production, we can be sure our environment is aligned across all places.

Devcontainers have seen massive developments and adoption over the past years. VSCode provides support for using Devcontainers and GitHub has been pushing their Codespaces: their completely managed remote Devcontainer service. Are you excited yet? Let's dive in. -->

<!-- ## The challenge: onboarding newcomers & mismatched environments -->

Take the following scenario. Your company uses Apache Spark to process data, and your team has pyspark set up in a Python project. The codebase is built on a specific Python version, using a certain Java installation, and an accompanying pyspark version that works with the former. To onboard a new member, you will need to pass a list of instructions the developer needs to follow carefully in order to get their setup working. But not everyone might run this on the same laptop environment: different hardware, and different operating systems. This is getting challenging.

But the setup is a one-off, right? Just go through the setup once and you’ll be good. Not entirely. Your code environment will change over time: your team will probably install, update or remove packages during the project’s development. This means that if a developer creates a new feature and changes their own environment to do so; he or she also needs to make sure that the other team members change theirs and that the production environment is updated accordingly. This makes it easy to get misaligned environments: between developers, and between development & production.

We can do better than this! Instead of giving other developers a setup document, let’s make sure we also create formal instructions so we can *automatically* set up the development environment. Docker lets us do exactly this – on which Devcontainers are built on top of. 
<!-- ~~Devcontainers to the rescue ⛑~~.  -->
Devcontainers can help us:

- 🔄 Get a reproducible development environment
- ⚡️ Instantly onboard new team members onto your project
- 👨‍👩‍👧‍👦 Better align the environments between team members
- ⏱ Keeping your dev environment up-to-date & reproducible saves your team time going into production later


Let’s explore how we can set up a Devcontainer for your Python project!

## Creating your first Devcontainer

<!-- > Step 1 -->

> This tutorial is focused on **VSCode**. Other IDE’s like PyCharm support running in Docker containers but support is less comprehensive than on VSCode.

### 📌 Recap

To recap, we are trying to create a dev environment that installs: 1) Java, 2) Python and 3) pyspark. And we want to do so *automatically*, that is, inside a Docker image.

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

That is, we have a Python module with an accompanying test, a `requirements.txt` file describing our production dependencies (pyspark), and a `requirements-dev.txt` describing dependencies that should be installed in development only (pytest, black, mypy). Now let’s see how we can extend this setup to include a Devcontainer.

### The `.devcontainer` folder

Your Devcontainer spec will live inside the `.devcontainer` folder. There will be two main files:

- `devcontainer.json`
- `Dockerfile`

Create a new file called `devcontainer.json`:

```json
{
    "build": {
        "dockerfile": "Dockerfile",
        "context": ".."
    }
}
```

This basically means: as a base for our Devcontainer, use the `Dockerfile` located in the current directory, and build it with a *current working directory* (cwd) of `..`.

So what does this `Dockerfile` look like?

```docker
FROM python:3.10

# Install Java
RUN apt update && \
    apt install -y sudo && \
    sudo apt install default-jdk -y

## Pip dependencies
# Upgrade pip
RUN pip install --upgrade pip
# Install production dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
# Install development dependencies
COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt && \
    rm /tmp/requirements-dev.txt
```

We are building our image on top of `python:3.10`, which is a Debian-based image. This is one of the Linux distributions that a Devcontainer can be built on. The main requirement is that **Node.js** should be able to run: VSCode automatically installs VSCode Server on the machine. For an extensive list of supported distributions, see [“Remote Development with Linux”](https://code.visualstudio.com/docs/remote/linux).

On top of `python:3.10`, we install Java and the required pip packages.

### Opening the Devcontainer

The `.devcontainer` folder is in place, so it’s now time to open our Devcontainer.

First, make sure you have the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed in VSCode (previously called “Remote - Containers”. That done, if you open your repo again, the extension should already detect your Devcontainer:

![folder contains a dev container config file](https://godatadriven.com/wp-content/uploads/2022/10/folder-contains-a-dev-container-config-file.png)

Alternatively, you can open up the command palette (<kbd>CMD</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) and select “*Dev Containers: Reopen in Container*”:

![Dev Containers: Reopen in Container](https://godatadriven.com/wp-content/uploads/2022/10/reopen-in-devcontainer-notification.png)

Your VSCode is now connected to the Docker container 🙌🏻:

![VSCode is now connected to the Docker container](https://godatadriven.com/wp-content/uploads/2022/10/opening-the-devcontainer.gif)

### What is happening under the hood 🚗

Besides starting the Docker image and attaching the terminal to it, VSCode is doing a couple more things:

1. [**VSCode Server**](https://code.visualstudio.com/docs/remote/vscode-server) is being installed on your Devcontainer. VSCode Server is installed as a service in the container itself so your VSCode installation can communicate with the container. For example, install and run extensions.
2. **Config is copied** over. Config like `~/.gitconfig` and `~/.ssh/known_hosts` are copied over to their respective locations in the container.
This then allows you to use your Git repo like you would do normally, without re-authenticating.
3. **Filesystem mounts**. VSCode automatically takes care of mounting: 1) The folder you are running the Devcontainer from and 2) your VSCode workspace folder.

### Opening your repo directly in a Devcontainer
Since all instructions on how to configure your dev environment are now defined in a Dockerfile, users can open up your Devcontainer with just one button:

[
    ![Open in Remote - Containers](
        https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode
    )
](
    https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/godatadriven/python-devcontainer-template
)

Ain't that cool? 🤩 You can add a button to your own repo like so:

```
[
    ![Open in Remote - Containers](
        https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode
    )
](
    https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/godatadriven/python-devcontainer-template
)
```

Just modify the GitHub URL ✓.

That said, we can see having built a Devcontainer can make our README massively more readable. What kind of README would you rather like?

Manual installation             |  Using a Devcontainer 🙌🏻
:-------------------------:|:-------------------------:
![](https://godatadriven.com/wp-content/uploads/2022/10/installation-instructions-manual.png)  |  ![](https://godatadriven.com/wp-content/uploads/2022/10/installation-instructions-devcontainer.png)

## Extending the Devcontainer

We have built a working Devcontainer, which is great! But a couple of things are still missing. We would like to:

- Install a non-root user for extra safety and good-practice
- Pass in custom VSCode settings and install extensions by default
- Be able to access Spark UI (port 4040)
- Run Continuous Integration (CI) in the Devcontainer

Let's see how.

### Installing a non-root user

<!-- > Step 2 -->

If you `pip install` a new package, you will see the following message:

![The warning message: “*WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: [https://pip.pypa.io/warnings/venv](https://pip.pypa.io/warnings/venv)*](https://godatadriven.com/wp-content/uploads/2022/10/running-pip-as-root.png)

Indeed, it is not recommended to develop as a _root_ user. It is considered a good practice to create a different user with fewer rights to run in production. So let's go ahead and create a user for this scenario.

<!-- > Running your application as a non-root user is recommended even in production (since it is more secure), so this is a good idea even if you're reusing an existing Dockerfile.
— [Add non-root user | VSCode Docs](https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user) -->

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

That's great! When we now start the container we should connect as the user `nonroot`.

### Passing custom VSCode settings

<!-- > Step 3 -->

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

The defined extensions are always installed in the Devcontainer. However, the defined settings provide just a **default** for the user to use, and can still be overridden by other setting scopes like User Settings, Remote Settings, or Workspace Settings.

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

Resulting in the Spark UI as we know it:

![spark UI in the browser](https://godatadriven.com/wp-content/uploads/2022/10/spark-ui-visible-in-localhost-4040.png)

✨

## Running our CI in the Devcontainer

Wouldn't it be convenient if we could re-use our Devcontainer to run our Continuous Integration (CI) pipeline as well? Indeed, we can do this with Devcontainers. Similarly to how the Devcontainer image is built locally using `docker build`, the same can be done _within_ a CI/CD pipeline. There are two basic options:

1. Build the Docker image _within_ the CI/CD pipeline
2. Prebuilding the image

To pre-build the image, the build step will need to run either periodically or whenever the Docker definition has changed. Since this adds quite some complexity let's dive into building the Devcontainer as part of the CI/CD pipeline first (for pre-building the image, see the 'Awesome resources' section). We will do so using **GitHub Actions**.

### Using `devcontainers/ci`

Luckily, a GitHub Action was already set up for us to do exactly this:

[https://github.com/devcontainers/ci](https://github.com/devcontainers/ci)

To now build, push and run a command in the Devcontainer is as easy as:

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

That's great! Whenever this workflow runs on your main branch, the image will be pushed to the configured registry; in this case GitHub Container Registry (GHCR). See below a trace of the executed GitHub Action:

![running-ci-in-the-devcontainer-github-actions](https://godatadriven.com/wp-content/uploads/2022/10/running-ci-in-the-devcontainer-github-actions.png)

Awesome!

<!-- ### Pre-building the image

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
``` -->

## The final Devcontainer definition

We built the following Devcontainer definitions. First, `devcontainer.json`:

```json
{
    "build": {
        "dockerfile": "Dockerfile",
        "context": ".."
    },

    "remoteUser": "nonroot",

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
    },

    "portsAttributes": {
        "4040": {
            "label": "SparkUI",
            "onAutoForward": "notify"
        }
    },

    "forwardPorts": [
        4040
    ]
}
```

And our `Dockerfile`:

```docker
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
USER $USERNAME

## Pip dependencies
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
```

> 📢 The full Devcontainer implementation and all the above steps can be found in the various branches of the [godatadriven/python-devcontainer-template](https://github.com/godatadriven/python-devcontainer-template) repo.

## Devcontainer architecture: Three environments 🎁

With the CI now set up, we can find that we can reuse the same Docker image for two purposes. For local development and running our quality checks. And, if we were to deploy this application to production, we could configure the Devcontainer to use our production image as a base, and install extra dependencies on top. If we would want to optimize the CI image to be as lightweight as possible, we could also strip off any extra dependencies that we do not require in the CI environment; things as extra CLI tooling, a better shell such as ZSH, and so forth.

This sets us up for having 3 different images for our entire lifecycle. One for Development, one for CI, and finally one for production. This can be visualized like so:

![three-environments-docker-images-devcontainer](https://godatadriven.com/wp-content/uploads/2022/10/three-environments-docker-images-devcontainer-setup.png)

So, we can see, when using a Devcontainer you can re-use your production image and build on top of it. Install extra tooling, make sure it can talk to VSCode, and you're done 🙏🏻. 

## Going further 🔮
There are lots of other resources to explore; Devcontainers are well-documented and there are many posts about it. If you're up for more, let's see what else you can do.
### Devcontainer features

Devcontainer [features](https://containers.dev/features) allow you to easily extend your Docker definition with common additions. Some useful features are:

- [Common Debian Utilities](https://github.com/devcontainers/features/tree/main/src/common-utils) (Installs ZSH using _Oh My ZSH_, a non-root user, and useful CLI tools like `curl`)
- [AWS CLI](https://github.com/devcontainers/features/tree/main/src/aws-cli)
- [Azure CLI](https://github.com/devcontainers/features/tree/main/src/azure-cli)
- [Git](https://github.com/devcontainers/features/tree/main/src/git)
- [Node.js](https://github.com/devcontainers/features/tree/main/src/node)
- [Python](https://github.com/devcontainers/features/tree/main/src/python)
- [Java](https://github.com/devcontainers/features/tree/main/src/java)

### Devcontainer templates
On the official Devcontainer specification website there are **loads** of templates available. Good chance (part of) your setup is in there. A nice way to get a head-start in building your Devcontainer or to get started quickly.

See: https://containers.dev/templates

### Mounting directories
Re-authenticating your CLI tools is annoying. So one trick is to mount your AWS/Azure/GCP credentials from your local computer into your Devcontainer. This way, authentications done in either environment are shared with the other. You can easily do this by adding this to `devcontainer.json`:

```json
  "mounts": [
    "source=/Users/<your_username>/.aws,target=/home/nonroot/.aws,type=bind,consistency=cached"
  ]
```

^ the above example mounts your AWS credentials, but the process should be similar for other cloud providers (GCP / Azure). 

<!-- ### Docker compose -->

### Awesome resources

- [devcontainers/ci](https://github.com/devcontainers/ci). Run your CI in your Devcontainers. Built on the [Devcontainer CLI](https://github.com/devcontainers/cli).
- [https://containers.dev/](https://containers.dev/). The official Devcontainer specification.
- [devcontainers/images](https://github.com/devcontainers/images). A collection of ready-to-use Devcontainer images.
- [Add a non-root user to a container](https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user). More explanations & instructions for adding a non-root user to your `Dockerfile` and `devcontainer.json`.
- [Pre-building dev container images](https://code.visualstudio.com/docs/remote/containers#_prebuilding-dev-container-images)
- [awesome-devcontainers](https://github.com/manekinekko/awesome-devcontainers). A repo pointing to yet even more awesome resources.

## Concluding
Devcontainers allow you to connect your IDE to a running Docker container, allowing for a native development experience but with the benefits of reproducibility and isolation. This makes easier to onboard new joiners and align development environments between team members. Devcontainers are very well supported for **VSCode** but are now being standardized in an [open specification](https://containers.dev/). Even though it will probably still take a while to see wide adoption, the specification is a good candidate for the standardization of Devcontainers.

🙌🏻

## About

This blogpost is written by [Jeroen Overschie](https://www.github.com/dunnkers), working at [GoDataDriven](https://godatadriven.com/).

&nbsp;

---

&nbsp;

GoDataDriven is a specialist in Data and AI, providing high-quality consultancy services for clients in The Netherlands and beyond. Do you feel right at home in the Data & AI space and are you interested? Look at our [Hiring](https://godatadriven.com/careers/) page.
