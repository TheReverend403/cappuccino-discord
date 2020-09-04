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

import shutil
import sys
from pathlib import Path

import yaml
from dotty_dict import Dotty

BASE_DIR = Path.cwd()
RESOURCE_ROOT = BASE_DIR / "cappuccino" / "resources"
CONFIG_ROOT = BASE_DIR / "config"

EX_CONFIG = 78  # EX_CONFIG from sysexits.h


class YamlConfig(Dotty):
    def __init__(self, filename="config.yml", required=False):
        super().__init__(dictionary={})

        self._default_path = RESOURCE_ROOT / "config" / filename
        self._path = CONFIG_ROOT / filename

        self._save_default(required=required)
        self.load(exit_on_error=True)

    def _save_default(self, required=False):
        if not self._path.exists():
            mkdir_args = {"parents": True, "exist_ok": True}
            if self._path.is_dir():
                self._path.mkdir(**mkdir_args)
            else:
                self._path.parent.mkdir(**mkdir_args)

            default_relative = self._default_path.relative_to(BASE_DIR)
            relative = self._path.relative_to(BASE_DIR)
            try:
                shutil.copy2(self._default_path, self._path)
                print(f"Copied {default_relative} to {relative}")
            except FileNotFoundError:
                return

            if required:
                print(f"{relative} requires configuration. Exiting now.")
                sys.exit(EX_CONFIG)

    def load(self, exit_on_error=False):
        # Load files in order of default -> local.
        for config_file in [self._default_path, self._path]:
            try:
                self.update(yaml.safe_load(config_file.read_text()))
            except (TypeError, FileNotFoundError):
                pass
            except yaml.YAMLError as exc:
                print(f"Error loading {config_file.relative_to(BASE_DIR)}: {exc}")
                if exit_on_error:
                    sys.exit(EX_CONFIG)


class LogConfig(YamlConfig):
    def __init__(self):
        super().__init__("logging.yml")


class BotConfig(YamlConfig):
    def __init__(self):
        super().__init__("config.yml", required=True)


class ExtensionConfig(YamlConfig):
    def __init__(self, extension):
        super().__init__(Path("extensions") / f"{extension.qualified_name.lower()}.yml")
