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
from pathlib import Path

import yaml
from dotty_dict import Dotty

BASE_DIR = Path.cwd()
RESOURCE_ROOT = BASE_DIR / 'cappuccino' / 'resources'
CONFIG_ROOT = BASE_DIR / 'config'


class YamlConfig(Dotty):

    def __init__(self, filename='config.yml', required=False):
        super().__init__(dictionary={})

        self._default_path = RESOURCE_ROOT / 'config' / filename
        self._path = CONFIG_ROOT / filename

        self._save_default(required=required)
        self.load(exit_on_error=True)

    def _save_default(self, required=False):
        if not self._path.exists():
            if self._path.is_dir():
                self._path.mkdir(parents=True, exist_ok=True)
            else:
                self._path.parent.mkdir(parents=True, exist_ok=True)

            try:
                shutil.copy2(self._default_path, self._path)
                print(f'Created a default config file at {self._path}')
            except FileNotFoundError:
                return

            if required:
                print(f'A default {os.path.basename(self._path)} has been created and must be configured.')
                sys.exit(0)

    def load(self, exit_on_error=False):
        # Load files in order of default -> local.
        for config_file in [self._default_path, self._path]:
            try:
                with config_file.open() as fd:
                    self.update(yaml.safe_load(fd))
            except (TypeError, FileNotFoundError):
                pass
            except yaml.YAMLError as exc:
                print(f'Error loading {config_file}: {exc}')
                if exit_on_error:
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
