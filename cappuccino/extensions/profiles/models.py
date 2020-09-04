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

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship

from cappuccino.database.models import Base


class Guild(Base):
    __tablename__ = "guilds"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=False)
    discriminator = Column(String, nullable=False)
    guild_members = relationship(
        "Nickname", backref="user", lazy=False, cascade="all, delete"
    )
    profile_fields = relationship(
        "ProfileField",
        order_by="ProfileField.list_position",
        backref="user",
        cascade="all, delete",
        collection_class=ordering_list("list_position", count_from=1),
    )


class ProfileField(Base):
    __tablename__ = "user_profiles"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    category = Column(String, primary_key=True)
    value = Column(String, primary_key=True)
    list_position = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now()
    )


class Nickname(Base):
    __tablename__ = "user_nicks"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guilds.id"), primary_key=True)
    nickname = Column(String, primary_key=True)
