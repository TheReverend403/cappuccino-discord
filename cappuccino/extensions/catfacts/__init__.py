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

from cappuccino.bot import Cappuccino
from cappuccino.extensions import Extension


class Catfacts(Extension):

    def __init__(self, bot: Cappuccino, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.cache = []
        self.limit = self.config.get('limit', 1000)
        self.max_length = self.config.get('max_length', 200)
        self.api_url = self.config.get(
            'api_url', 'https://catfact.ninja/facts?limit={limit}&max_length={max_length}') \
            .format(limit=self.limit, max_length=self.max_length)

    def get_fact(self):
        if len(self.cache) > 0:
            return self.cache.pop()

        with self.bot.requests.get(self.api_url) as response:
            self.logger.debug('Fetching cat facts.')
            self.cache = [fact['fact'] for fact in response.json()['data']]
            random.shuffle(self.cache)
            return self.get_fact()

    @commands.command(aliases=['cf'], brief='Get a random cat fact.')
    async def catfact(self, ctx: commands.Context):
        try:
            async with ctx.typing():
                fact = self.get_fact()
            await ctx.send(fact)
        except RequestException as exc:
            self.logger.exception(exc)
            await ctx.send(f'Something terrible happened while I was researching cat facts. Sorry. :(')


def setup(bot: Cappuccino):
    bot.add_cog(Catfacts(bot))
