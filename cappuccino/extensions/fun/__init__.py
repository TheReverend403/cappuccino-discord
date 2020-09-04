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

from aiohttp import ClientError
from discord.ext import commands
from discord.utils import escape_markdown

from cappuccino import Cappuccino
from cappuccino.extensions import Extension


class Fun(Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @commands.command(aliases=["whatthecommit"])
    async def wtc(self, ctx: commands.Context):
        """Get a random commit message from whatthecommit.com."""
        try:
            async with ctx.typing(), self.bot.requests.get(
                "http://whatthecommit.com/index.txt"
            ) as response:
                commit_message = await response.text()
                commit_message = escape_markdown(commit_message.strip())
            await ctx.send(commit_message)
        except ClientError as exc:
            self.logger.exception(f"Error fetching commit message: {exc}")
            await ctx.send(
                (
                    "Failed to get commit message. "
                    "Why do you always have to break everything? e.e"
                )
            )


def setup(bot: Cappuccino):
    bot.add_cog(Fun(bot))
