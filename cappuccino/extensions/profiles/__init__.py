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

from discord import Guild, Member, Message, User
from discord.ext.commands.cog import Cog

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
        self.db.update_user(after)

    @humans_only
    @Cog.listener()
    async def on_member_join(self, member: Member):
        self.db.update_user(member)

    @humans_only
    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if before.nick == after.nick:
            return
        self.db.update_user(after)

    @Cog.listener()
    async def on_guild_available(self, guild: Guild):
        self.db.update_guild(guild)

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        self.db.update_guild(guild)

    @Cog.listener()
    async def on_guild_update(self, before: Guild, after: Guild):
        self.db.update_guild(after)


def setup(bot: Cappuccino):
    bot.add_cog(Profiles(bot))
