<p align="center">
<img src="https://static.foxdev.co/img/catpuccino_alpha_128.png">
</p>

<h1 align="center">cappuccino-discord</h1>

<p align="center">
<a href="LICENSE"><img src="https://img.shields.io/github/license/FoxDev/cappuccino-discord?style=flat-square" alt="GitHub"></a>
<a href="https://github.com/FoxDev/cappuccino-discord/actions"><img src="https://img.shields.io/github/workflow/status/FoxDev/cappuccino-discord/ci?style=flat-square" alt="GitHub Workflow Status"></a>
<a href="https://requires.io/github/FoxDev/cappuccino-discord/requirements"><img src="https://img.shields.io/requires/github/FoxDev/cappuccino-discord?style=flat-square" alt="Requires.io"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="Code style: black"></a>
</p>

<p align="center">
Nothing fancy, just an experimental Discord port of <a href="https://github.com/FoxDev/cappuccino">cappuccino</a> for fun.
</p>

## Installation

Requirements:
* PostgreSQL
* Redis
* Python 3.8+
* [Poetry](https://python-poetry.org)
* [A Discord bot account](https://discordpy.readthedocs.io/en/latest/discord.html)

```shell script
git clone https://github.com/FoxDev/cappuccino-discord
cd cappuccino-discord
poetry install
poetry shell
python -m cappuccino
# Configure the bot with the newly created configs.
# then...
python -m cappuccino
```

Optional: Install [the included unit file](cappuccino/resources/cappuccino-discord.service) to run the bot under systemd.

## Developers
[pre-commit](https://pre-commit.com/) is used for formatting and PEP 8 compliance checks.

These checks must pass in order to make a commit to `master`. To install and use the hooks, run the following commands:

```shell script
poetry shell # If you're not already in the poetry env.
pre-commit install
pre-commit run --all-files # or just make a commit to run checks automatically.
```
