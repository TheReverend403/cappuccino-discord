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

from discord.ext import commands
from discord.utils import escape_markdown
from httpx import RequestError

from cappuccino.bot import Cappuccino
from cappuccino.extensions import Extension


class Fun(Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @commands.command(aliases=["whatthecommit"])
    async def wtc(self, ctx: commands.Context):
        """Get a random commit message from whatthecommit.com."""
        try:
            async with ctx.typing(), self.bot.httpx as client:
                response = await client.get("http://whatthecommit.com/index.txt")
                response.raise_for_status()
                commit_message = response.text
                commit_message = escape_markdown(commit_message.strip())
            await ctx.send(commit_message)
        except RequestError:
            self.logger.exception("Error fetching commit message.")
            await ctx.send(
                "Failed to get commit message. Why do you always break everything? e.e"
            )


def setup(bot: Cappuccino):
    bot.add_cog(Fun(bot))
