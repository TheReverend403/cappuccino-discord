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

import logging
from typing import Type

from discord import Guild, Member, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cappuccino.database.models import GuildMember


class Database(object):
    bot = None

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('cappuccino.database')
        self.bot = bot
        _Session = sessionmaker(bind=create_engine(self.bot.config.get('database').get('uri')))
        self.session = _Session()

    def __getattr__(self, name: str):
        return getattr(self.session, name) or getattr(self, name)

    def update_user(self, user: Type[User]):
        self.logger.debug(f'update_user({user})')
        user_model = self.session.query(models.User).filter_by(discord_id=user.id).first()

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
            member = self.session.query(GuildMember).filter_by(guild_id=user.guild.id, user_id=user.id).first()
            if not member:
                member = GuildMember(user_id=user.id, guild_id=user.guild.id, nickname=user.nick)
            else:
                member.nickname = member.nickname
            self.session.add(member)
            self.logger.debug(f'set_nick({user}, {user.nick})')

        self.session.add(user_model)
        self.session.commit()

    def update_guild(self, discord_guild: Guild):
        guild = self.session.query(models.Guild).filter_by(discord_id=discord_guild.id).first()
        guild_name = discord_guild.name
        guild_description = discord_guild.description

        if guild:
            guild.name = guild_name
            guild.description = guild_description
        else:
            guild = models.Guild(discord_id=discord_guild.id,
                                 name=guild_name,
                                 description=guild_description)

        self.session.add(guild)
        self.session.commit()
