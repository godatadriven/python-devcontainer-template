# python-devcontainer-template
An example repo for using a Devcontainer + Python 🐳🐍.

[Devcontainers](https://containers.dev/) help us:

- 🔄 Get a reproducible development environment
- ⚡️ Instantly onboard new team members onto your project
- 👨‍👩‍👧‍👦 Better align the environments between team members
- ⏱ Keeping your dev environment up-to-date & reproducible saves your team time going into production later

(📝 Note: Devcontainers are a relatively new concept. For now, Devcontainers are only properly supported by **VSCode**.)

## This template
This template demonstrates how you can build a Devcontainer with the following set up:

- Python 3.10
- Java (OpenJDK 11.0.16)
- `pyspark`, `mypy`, `pytest` and `black`

## Usage

> First, make sure you have the [Remote Development extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) installed and have [Docker](https://www.docker.com/products/docker-desktop/) running.

Then, there's 2 options:

### Using the template

1. Click _Use this template_ to create a new repo.

    <a href="https://github.com/godatadriven/python-devcontainer-template/generate"><img alt="use this template GitHub button" src="https://github.com/godatadriven/python-devcontainer-template/assets/744430/8cb7bc77-af79-41cd-b9da-5625e7ba843e" width="150px" /></a>

1. **Clone** the repo and open it in **VSCode**.

1. You should see the following notification:

    <img src="https://raw.githubusercontent.com/godatadriven/python-devcontainer-template/blogpost/images/folder-contains-a-dev-container-config-file.png" alt="folder contains a dev container config file" width="500px"/>

    Press _Reopen in Container_ and you the Devcontainer will be loaded.


That's it 🙌🏻 Enjoy developing.

### Using the button

Another option is to open this repo in VSCode using a special _link_. Press the following button:

[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/godatadriven/python-devcontainer-template)

🚀 This clones this repo and opens it in a Devcontainer right away.

- 💡 To now have this repo push to your own repo, add a different Git remote using `git remote add`.

## About

### Media
This repo was mentioned at the following places:

- [Talk @ GoDataFest](https://godatafest.com/broadcasts/devcontainers-containerize-your-development-setup/), 26th of October [[talk slides](https://godatadriven.github.io/python-devcontainer-template/#/)]
- [Blogpost @ godatadriven.com](https://godatadriven.com/blog/how-to-create-a-devcontainer-for-your-python-project-%F0%9F%90%B3/), 21st of November
- [Talk @ PyData Eindhoven](https://www.youtube.com/watch?v=SLsaCdRAV0U)

---


Created by [Jeroen Overschie](https://www.github.com/dunnkers), working at [Xebia Data](https://xebia.com/). A leading Data and AI consultancy company in The Netherlands.
