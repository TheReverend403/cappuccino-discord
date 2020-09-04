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
from logging.config import dictConfig

from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands import Bot, ExtensionError
from redis import Redis
from sqlalchemy.orm import Session

from cappuccino.config import Config, LogConfig
from cappuccino.database import get_session

dictConfig(dict(LogConfig()))


def _get_version():
    try:
        return subprocess.check_output(["git", "describe"]).decode("UTF-8").strip()
    except subprocess.CalledProcessError:
        return "0.5.0"


def create_bot():
    bot = Cappuccino(Config())
    return bot


class Cappuccino(Bot):
    def __init__(self, botconfig: Config, *args, **kwargs):
        self.version = _get_version()
        self.logger = logging.getLogger("cappuccino")
        self.config = botconfig
        self.database: Session = get_session(self.config.get("database.uri"))
        self.requests = ClientSession(
            headers={"User-Agent": f"cappuccino-discord ({self.version})"}
        )
        self.cache: Redis = Redis.from_url(
            self.config.get("redis.uri"), decode_responses=True
        )

        super().__init__(
            command_prefix=self.config.get("bot.command_prefix", "."), *args, **kwargs
        )

    def load_extensions(self):
        # Ensure core extensions are always forced to load
        # before anything else regardless of user preference.
        extensions = ["core", "profiles"]
        extensions.extend(self.config.get("extensions", []))

        for extension in extensions:
            try:
                self.load_extension(f"cappuccino.extensions.{extension}")
                self.logger.info(f"Enabled extension '{extension}'")
            except ExtensionError as exc:
                self.logger.exception(
                    f"Error occurred while loading '{extension}': {exc}"
                )

    async def on_connect(self):
        self.logger.info("Connected to Discord.")

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} and ready to go to work.")

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.UserInputError):
            await ctx.send({exception})
            return

        raise exception

    # Override parent method to allow messages from other bots such as DiscordSRV.
    # https://github.com/Rapptz/discord.py/issues/2238
    async def process_commands(self, message):
        if self.config.get("bot.ignore_bots", False) and message.author.bot:
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)

    def run(self, *args, **kwargs):
        token = self.config.get("bot.token")
        super().run(token, *args, **kwargs)
