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

from datetime import timedelta

from aiohttp import ClientError
from discord.ext import commands
from discord.utils import escape_markdown

from cappuccino import Cappuccino
from cappuccino.extensions import Extension


class Catfacts(Extension):
    _cache_key = "catfacts"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = self.bot.cache
        self.limit = self.config.get("limit", 1000)
        self.max_length = self.config.get("max_length", 200)
        self.cache_ttl = self.config.get("cache_ttl", 72)
        self.api_url = self.config.get("api_url", "https://catfact.ninja/facts")

    async def get_fact(self):
        if self.cache.scard(self._cache_key) > 0:
            return self.cache.spop(self._cache_key)

        params = {"limit": self.limit}
        if self.max_length > 0:
            params.update({"max_length": self.max_length})

        self.logger.debug("Fetching cat facts.")
        async with self.bot.requests.get(self.api_url, params=params) as response:
            facts = await response.json()
            facts = [fact["fact"] for fact in facts["data"]]
            self.logger.debug(f"Fetched {len(facts)} facts.")
            self.cache.sadd(self._cache_key, *facts)
            self.cache.expire(self._cache_key, timedelta(hours=self.cache_ttl))
            return await self.get_fact()

    @commands.command(aliases=["cf"])
    async def catfact(self, ctx: commands.Context):
        """Get a random cat fact."""
        try:
            async with ctx.typing():
                fact = await self.get_fact()
            await ctx.send(escape_markdown(fact))
        except ClientError as exc:
            self.logger.exception(exc)
            await ctx.send(
                (
                    "Something terrible happened while I was researching cat facts."
                    "Sorry. :("
                )
            )


def setup(bot: Cappuccino):
    bot.add_cog(Catfacts(bot))
