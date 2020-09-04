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

import os
import shutil
import sys

import yaml
from dotty_dict import Dotty


class YamlConfig(Dotty):
    _base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _config_dir = os.path.join(_base_dir, 'config')
    _resource_dir = os.path.join(_base_dir, 'cappuccino', 'resources', 'config')

    def __init__(self, filename='config.yml', required=False):
        super().__init__(dictionary={})

        self.default_path = os.path.join(self._resource_dir, filename)
        self.local_path = os.path.join(self._config_dir, filename)

        if not os.path.exists(self.local_path):
            os.makedirs(os.path.dirname(self.local_path), exist_ok=True)
            try:
                shutil.copy2(self.default_path, self.local_path)
                print(f'Created a default config file at {self.local_path}')
            except FileNotFoundError:
                return

            if required:
                print(f'A default {os.path.basename(filename)} has been created and must be configured.')
                sys.exit(0)

        # Load files in order of default -> local.
        for config_file in [self.default_path, self.local_path]:
            try:
                with open(config_file) as fd:
                    self.update(yaml.safe_load(fd))
            except (TypeError, FileNotFoundError):
                pass
            except yaml.YAMLError as exc:
                print(f'Error loading {config_file}: {exc}')
                sys.exit(78)  # EX_CONFIG from sysexits.h


class LogConfig(YamlConfig):

    def __init__(self):
        super().__init__('logging.yml')


class BotConfig(YamlConfig):

    def __init__(self):
        super().__init__('config.yml', required=True)


class ExtensionConfig(YamlConfig):

    def __init__(self, extension):
        super().__init__(os.path.join('extensions', f'{extension.qualified_name.lower()}.yml'))
