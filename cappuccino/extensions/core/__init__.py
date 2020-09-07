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
from discord import Color, Embed
from discord.ext import commands
from discord.ext.commands import (
    is_owner,
    ExtensionError,
    ExtensionNotLoaded,
    ExtensionNotFound,
    ExtensionAlreadyLoaded,
)

from cappuccino import Cappuccino
from cappuccino.extensions import Extension

ERROR_PREFIX = "🔴"
SUCCESS_PREFIX = "🟢"
EXTENSION_MODULE_PREFIX = "cappuccino.extensions"


class Core(Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @commands.command(aliases=["bots", "ver"])
    async def version(self, ctx: commands.Context):
        """Show version info."""
        python_version = platform.python_version()
        discord_ver = discord.version_info
        color = (254, 167, 71)  # Orange, FEA747

        embed = Embed(
            title="capuccino-discord",
            url="https://github.com/FoxDev/cappuccino-discord",
            description="An experimental port of https://github.com/FoxDev/cappuccino",
            color=Color.from_rgb(*color),
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Version", value=self.bot.version, inline=False)
        embed.add_field(name="Python", value=python_version)
        embed.add_field(
            name="discord.py",
            value=f"{discord_ver.major}.{discord_ver.minor}.{discord_ver.micro}",
        )

        await ctx.send(embed=embed)

    @commands.command()
    @is_owner()
    async def unload(self, ctx: commands.Context, extension: str):
        try:
            self.bot.unload_extension(f"{EXTENSION_MODULE_PREFIX}.{extension}")
            await ctx.send(f"{SUCCESS_PREFIX} Unloaded **{extension}**.")
        except ExtensionNotLoaded:
            await ctx.send(f"{ERROR_PREFIX} **{extension}** is already unloaded.")

    @commands.command()
    @is_owner()
    async def load(self, ctx: commands.Context, extension: str):
        try:
            self.bot.load_extension(f"{EXTENSION_MODULE_PREFIX}.{extension}")
            await ctx.send(f"{SUCCESS_PREFIX} Loaded **{extension}**.")
        except ExtensionNotFound:
            await ctx.send(f"{ERROR_PREFIX} Could not find **{extension}**.")
        except ExtensionAlreadyLoaded:
            await ctx.send(f"{ERROR_PREFIX} **{extension}** is already loaded.")
        except ExtensionError as exc:
            self.logger.exception(exc)
            await ctx.send(f"{ERROR_PREFIX} Failed to load **{extension}**: {exc}")

    @commands.command()
    @is_owner()
    async def reload(self, ctx: commands.Context, extension: str):
        try:
            self.bot.reload_extension(f"{EXTENSION_MODULE_PREFIX}.{extension}")
            await ctx.send(f"{SUCCESS_PREFIX} **{extension}** reloaded successfully.")
        except ExtensionNotFound:
            await ctx.send(f"{ERROR_PREFIX} Could not find **{extension}**.")
        except ExtensionNotLoaded:
            await ctx.send(f"{ERROR_PREFIX} **{extension}** is not loaded.")
        except ExtensionError as exc:
            self.logger.exception(exc)
            await ctx.send(f"{ERROR_PREFIX} Failed to reload **{extension}**.: {exc}")


def setup(bot: Cappuccino):
    bot.add_cog(Core(bot))
