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

import functools
from typing import Type

import discord
from discord.ext.commands.cog import Cog

from cappuccino import Cappuccino
from cappuccino.extensions import Extension
from .models import Guild, GuildMember, User


def humans_only(func):
    """We don't really care about storing bot info, real users only."""

    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        for arg in args:
            if isinstance(arg, discord.Message) and (arg.author.bot or arg.author.system):
                return
        await func(*args, **kwargs)

    return decorator


class Profiles(Extension):

    def __init__(self, bot: Cappuccino, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.db = self.bot.database

    @Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.update_guild(guild)
            for member in guild.members:
                if member.bot or member.system:
                    continue
                self.update_user(member)

    @humans_only
    @Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        if before.name == after.name and before.discriminator == after.discriminator:
            return
        self.update_user(after)

    @humans_only
    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        self.update_user(member)

    @humans_only
    @Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.nick == after.nick:
            return
        self.update_user(after)

    @Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        self.update_guild(guild)

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.update_guild(guild)
        for member in guild.members:
            if member.bot or member.system:
                continue
            self.update_user(member)

    @Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        if before.name == after.name:
            return
        self.update_guild(after)

    def update_user(self, user: Type[discord.User]):
        user_model = self.db.query(User).filter_by(id=user.id).first()

        if user_model:
            if user_model.username != user.name or user_model.discriminator != user.discriminator:
                user_model.username = user.name
                user_model.discriminator = user.discriminator
        else:
            user_model = User(id=user.id, username=user.name, discriminator=user.discriminator)
            self.db.add(user_model)

        if user_model in self.db.dirty:
            self.logger.debug(f'update_user({user})')

        if isinstance(user, discord.Member):
            guild_member = self.db.query(GuildMember).filter_by(guild_id=user.guild.id, user_id=user.id).first()

            if guild_member:
                if user.nick is None:
                    self.db.delete(guild_member)
                if guild_member.nickname != user.nick:
                    guild_member.nickname = user.nick
            elif user.nick is not None:
                guild_member = GuildMember(user_id=user.id, guild_id=user.guild.id, nickname=user.nick)
                self.db.add(guild_member)

            if guild_member in self.db.dirty:
                self.logger.debug(f'set_nick({user}, {user.nick}, {user.guild.id})')

        self.db.commit()

    def update_guild(self, guild: Guild):
        guild_model = self.db.query(Guild).filter_by(id=guild.id).first()
        guild_name = guild.name
        guild_description = guild.description

        if guild_model:
            guild_model.name = guild_name
            guild_model.description = guild_description
        else:
            guild_model = Guild(id=guild.id, name=guild_name, description=guild_description)

        self.db.add(guild_model)
        self.db.commit()


def setup(bot: Cappuccino):
    bot.add_cog(Profiles(bot))
