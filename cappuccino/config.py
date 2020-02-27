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
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir, 'config')
    resource_dir = os.path.join(base_dir, 'cappuccino', 'resources')
    config_required = False  # If true, copy the default file and then exit.

    def __init__(self, filename='config.yml'):
        super().__init__()

        self.default_path = os.path.join(self.resource_dir, filename)
        self.local_path = os.path.join(self.config_dir, filename)

        if not os.path.exists(f'{self.local_path}'):
            try:
                os.mkdir(self.config_dir)
            except FileExistsError:
                pass

            if self.config_required:
                shutil.copy2(self.default_path, self.local_path)
                print(f'A default {filename} has been created and must be configured.')
                exit(1)

        # Load files in order of default -> local.
        for config_file in [self.default_path, self.local_path]:
            try:
                with open(config_file) as fd:
                    self.update(yaml.safe_load(fd))
            except FileNotFoundError:
                pass


class LogConfig(YamlConfig):

    def __init__(self):
        super().__init__('logging.yml')


class BotConfig(YamlConfig):

    config_required = True

    def __init__(self):
        super().__init__('config.yml')
