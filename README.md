# cappuccino-discord

[![GitHub](https://img.shields.io/github/license/FoxDev/cappuccino-discord?style=flat-square)](LICENSE)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/FoxDev/cappuccino-discord/ci?style=flat-square)](https://github.com/FoxDev/cappuccino-discord/actions)
[![Requires.io](https://img.shields.io/requires/github/FoxDev/cappuccino-discord?style=flat-square)](https://requires.io/github/FoxDev/cappuccino-discord/requirements)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

Nothing fancy, just an experimental Discord port of [cappuccino](https://github.com/FoxDev/cappuccino) for fun.

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

Install this repo's pre-commit hooks with `pre-commit install`

All commits must pass `pre-commit run --all-files`
