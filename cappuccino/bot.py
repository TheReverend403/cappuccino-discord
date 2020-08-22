#  This file is part of cappuccino-discord.
#
#  cappuccino-discord is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  cappuccino-discord is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with cappuccino-discord.  If not, see <https://www.gnu.org/licenses/>.

import logging
import subprocess

import requests
from discord.ext import commands
from discord.ext.commands import Bot, ExtensionError

from cappuccino.database import Database
from config import BotConfig


def _get_version():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('UTF-8').strip()


class Cappuccino(Bot):

    def __init__(self, config: BotConfig, *args, **kwargs):
        self.version = _get_version()
        self.logger = logging.getLogger('cappuccino')
        self.config = config
        self.database = Database(self)
        self.requests = requests.Session()
        self.requests.headers.update({'User-Agent': f'cappuccino-discord ({self.version})'})

        super().__init__(command_prefix=self.config.get('bot').get('command_prefix', '.'), *args, **kwargs)

        for extension in self.config.get('extensions', []):
            try:
                self.load_extension(f'extensions.{extension}')
            except ExtensionError as exc:
                self.logger.exception(f'Error occurred while loading \'{extension}\': {exc}')
            else:
                self.logger.info(f'Enabled extension \'{extension}\'')

    async def on_connect(self):
        self.logger.info(f'Connected to Discord.')

    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user} and ready to go to work.')

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            await ctx.send(f'{exception}')

    # Override parent method to allow messages from other bots such as DiscordSRV.
    # https://github.com/Rapptz/discord.py/issues/2238
    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    def run(self, *args, **kwargs):
        token = self.config.get('discord').get('token')
        super().run(token, *args, **kwargs)
