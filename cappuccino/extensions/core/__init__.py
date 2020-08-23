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

import discord
from discord import Embed
from discord.ext import commands

from cappuccino.bot import Cappuccino
from cappuccino.extensions import Extension


class Core(Extension):

    def __init__(self, bot: Cappuccino, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)

    @commands.command(aliases=['bots', 'ver'])
    async def version(self, ctx: commands.Context):
        """Show version info."""
        python_version = platform.python_version()
        discord_version = discord.version_info

        embed = Embed(title='capuccino-discord',
                      url='https://github.com/FoxDev/cappuccino-discord',
                      description='An experimental port of https://github.com/FoxDev/cappuccino')
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Version', value=self.bot.version, inline=False)
        embed.add_field(name='Python', value=python_version)
        embed.add_field(name='discord.py',
                        value=f'{discord_version.major}.{discord_version.minor}.{discord_version.micro}')

        await ctx.send(embed=embed)


def setup(bot: Cappuccino):
    bot.add_cog(Core(bot))
