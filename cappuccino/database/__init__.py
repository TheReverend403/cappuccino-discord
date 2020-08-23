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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database(object):
    bot = None

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('cappuccino.database')
        self.bot = bot
        self.session = sessionmaker(bind=create_engine(self.bot.config.get('database').get('uri')))()

    def __getattr__(self, name: str):
        return getattr(self.session, name) or getattr(self, name)
