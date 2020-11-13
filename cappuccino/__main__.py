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

import sentry_sdk
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from cappuccino import create_bot


def init_sentry(bot):
    dsn = bot.config.get("sentry.dsn", "")
    if not dsn:
        bot.logger.debug("Missing Sentry DSN, sentry will not be used.")
        return

    sentry_sdk.init(
        dsn,
        integrations=[SqlalchemyIntegration(), RedisIntegration()],
        release=bot.version,
    )
    bot.logger.info("Sentry logging enabled.")


def main():
    bot = create_bot()
    init_sentry(bot)
    bot.load_extensions()
    bot.run()


if __name__ == "__main__":
    main()
