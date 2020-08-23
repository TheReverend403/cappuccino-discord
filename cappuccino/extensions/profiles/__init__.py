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

from discord import Guild, Member, Message, User
from discord.ext.commands.cog import Cog

import cappuccino.extensions.profiles.models
from cappuccino.bot import Cappuccino
from cappuccino.extensions import Extension


def humans_only(func):
    """We don't really care about storing bot info, real users only."""

    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        for arg in args:
            if isinstance(arg, Message) and (arg.author.bot or arg.author.system):
                return
        await func(*args, **kwargs)

    return decorator


class Profiles(Extension):

    def __init__(self, bot: Cappuccino, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.db = self.bot.database

    @humans_only
    @Cog.listener()
    async def on_user_update(self, before: User, after: User):
        self.update_user(after)

    @humans_only
    @Cog.listener()
    async def on_member_join(self, member: Member):
        self.update_user(member)

    @humans_only
    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if before.nick == after.nick:
            return
        self.update_user(after)

    @Cog.listener()
    async def on_guild_available(self, guild: Guild):
        self.update_guild(guild)

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        self.update_guild(guild)

    @Cog.listener()
    async def on_guild_update(self, before: Guild, after: Guild):
        self.update_guild(after)

    def update_user(self, user: Type[User]):
        self.logger.debug(f'update_user({user})')
        user_model = self.db.query(models.User).filter_by(discord_id=user.id).first()

        if user_model:
            user_model.name = user.name
            user_model.discriminator = user.discriminator
        else:
            user_model = models.User(
                discord_id=user.id,
                username=user.name,
                discriminator=user.discriminator
            )

        if isinstance(user, Member) and user.nick is not None:
            member = self.db.query(models.GuildMember).filter_by(guild_id=user.guild.id, user_id=user.id).first()
            if not member:
                member = models.GuildMember(user_id=user.id, guild_id=user.guild.id, nickname=user.nick)
            else:
                member.nickname = member.nickname
            self.db.add(member)
            self.logger.debug(f'set_nick({user}, {user.nick})')

        self.db.add(user_model)
        self.db.commit()

    def update_guild(self, discord_guild: Guild):
        guild = self.db.query(models.Guild).filter_by(discord_id=discord_guild.id).first()
        guild_name = discord_guild.name
        guild_description = discord_guild.description

        if guild:
            guild.name = guild_name
            guild.description = guild_description
        else:
            guild = models.Guild(discord_id=discord_guild.id,
                                 name=guild_name,
                                 description=guild_description)

        self.db.add(guild)
        self.db.commit()


def setup(bot: Cappuccino):
    bot.add_cog(Profiles(bot))

