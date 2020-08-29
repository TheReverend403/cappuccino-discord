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

from discord.ext.commands import Cog

from cappuccino import Cappuccino


class Extension(Cog):

    def __init__(self, bot: Cappuccino, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.logger = logging.getLogger(f'cappuccino.extension.{self.qualified_name.lower()}')
        self.config: dict = self.bot.config.get(f'extensions.{self.qualified_name.lower()}', {})
