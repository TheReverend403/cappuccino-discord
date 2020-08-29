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

import random

from aiohttp import ClientError
from discord.ext import commands
from discord.utils import escape_markdown

from cappuccino import Cappuccino
from cappuccino.extensions import Extension


class Catfacts(Extension):

    def __init__(self, bot: Cappuccino, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.cache = []
        self.limit = self.config.get('limit', 1000)
        self.max_length = self.config.get('max_length', 0)
        self.api_url = self.config.get('api_url', f'https://catfact.ninja/facts?limit={self.limit}')

        if self.max_length > 0:
            self.api_url += f'&max_length={self.max_length}'

    async def get_fact(self):
        if len(self.cache) > 0:
            return self.cache.pop()

        async with self.bot.requests.get(self.api_url) as response:
            self.logger.debug('Fetching cat facts.')
            self.cache = [fact['fact'] for fact in (await response.json())['data']]
            self.logger.debug(f'Fetched {len(self.cache)} facts.')
            random.shuffle(self.cache)
            return await self.get_fact()

    @commands.command(aliases=['cf'])
    async def catfact(self, ctx: commands.Context):
        """Get a random cat fact."""
        try:
            async with ctx.typing():
                fact = await self.get_fact()
            await ctx.send(escape_markdown(fact))
        except ClientError as exc:
            self.logger.exception(exc)
            await ctx.send(f'Something terrible happened while I was researching cat facts. Sorry. :(')


def setup(bot: Cappuccino):
    bot.add_cog(Catfacts(bot))
