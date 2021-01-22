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

from discord.ext import commands
from discord.utils import escape_markdown
from httpx import RequestError

from cappuccino.bot import Cappuccino
from cappuccino.extensions import Extension


class Catfacts(Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = []
        self._limit = self.config.get("limit", 1000)
        self._max_length = self.config.get("max_length", 200)
        self._api_url = self.config.get("api_url", "https://catfact.ninja/facts")

    async def get_fact(self):
        if len(self._cache) > 0:
            return self._cache.pop()

        params = {"limit": self._limit}
        if self._max_length > 0:
            params.update({"max_length": self._max_length})

        self.logger.debug("Fetching cat facts.")
        async with self.bot.httpx as client:
            response = await client.get(self._api_url, params=params)
            response.raise_for_status()
            facts = response.json()
            self._cache = [fact["fact"] for fact in facts["data"]]
            random.shuffle(self._cache)
            self.logger.debug(f"Fetched {len(self._cache)} facts.")
            return await self.get_fact()

    @commands.command(aliases=["cf"])
    async def catfact(self, ctx: commands.Context):
        """Get a random cat fact."""
        try:
            async with ctx.typing():
                fact = await self.get_fact()
            await ctx.send(escape_markdown(fact))
        except RequestError:
            self.logger.exception("Error fetching cat facts.")
            await ctx.send(
                "Something went wrong while I was researching cat facts. Sorry. :("
            )


def setup(bot: Cappuccino):
    bot.add_cog(Catfacts(bot))
