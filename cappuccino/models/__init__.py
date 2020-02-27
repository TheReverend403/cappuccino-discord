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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    discord_id = Column(BigInteger, primary_key=True)
    profile_fields = relationship('UserProfileField',
                                  order_by='UserProfileField.list_position', backref='user',
                                  collection_class=ordering_list('list_position', count_from=1))


class UserProfileField(Base):
    __tablename__ = 'user_profile_fields'

    user_id = Column(BigInteger, ForeignKey('users.discord_id'), primary_key=True)
    category = Column(String, primary_key=True)
    value = Column(String, primary_key=True)
    list_position = Column(Integer, nullable=False)
    updated_at = Column(DateTime(), nullable=False, server_default=func.now(), server_onupdate=func.now())
