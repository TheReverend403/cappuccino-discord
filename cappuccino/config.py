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

import yaml


class YamlConfig(dict):
    _base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _config_dir = os.path.join(_base_dir, 'config')
    _resource_dir = os.path.join(_base_dir, 'cappuccino', 'resources')
    _must_be_configured = False  # If true, copy the default file and then exit.

    def __init__(self, filename='config.yml'):
        super().__init__()

        self._default_path = os.path.join(self._resource_dir, filename)
        self._local_path = os.path.join(self._config_dir, filename)

        if not os.path.exists(f'{self._local_path}'):
            try:
                os.mkdir(self._config_dir)
            except FileExistsError:
                pass

            if self._must_be_configured:
                shutil.copy2(self._default_path, self._local_path)
                print(f'A default {filename} has been created and must be configured.')
                exit(1)

        # Load files in order of default -> local.
        for config_file in [self._default_path, self._local_path]:
            try:
                with open(config_file) as fd:
                    self.update(yaml.safe_load(fd))
            except FileNotFoundError:
                pass


class LogConfig(YamlConfig):

    def __init__(self):
        super().__init__('logging.yml')


class BotConfig(YamlConfig):

    _must_be_configured = True

    def __init__(self):
        super().__init__('config.yml')
