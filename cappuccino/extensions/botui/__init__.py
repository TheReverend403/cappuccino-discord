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

import platform

from discord.ext import commands

from cappuccino.bot import Cappuccino
from cappuccino.extensions import Extension


class BotUI(Extension):

    def __init__(self, bot: Cappuccino, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)

    @commands.command(aliases=['version'], brief='Show version info.')
    async def bots(self, ctx: commands.Context):
        pyver = platform.python_version()
        await ctx.send(f'Reporting in! (cappuccino-discord {self.bot.version}, Python {pyver})')


def setup(bot: Cappuccino):
    bot.add_cog(BotUI(bot))
