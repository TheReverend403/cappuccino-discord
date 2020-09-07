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

from cappuccino.config.errors import NotConfiguredError

BASE_DIR = Path(__file__).parent.parent
RESOURCE_ROOT = BASE_DIR / "resources"
CONFIG_ROOT = BASE_DIR.parent / "config"


class YamlConfig(Dotty):
    def __init__(self, filename="config.yml", required=False, required_keys=None):
        super().__init__(dictionary={})

        if required_keys is None:
            required_keys = []

        self._required = required
        self._required_keys = required_keys
        self.default_file_path = RESOURCE_ROOT / "config" / filename
        self.file_path = CONFIG_ROOT / filename

    def save_default(self):
        if not self.default_file_path.exists() or self.file_path.exists():
            return

        mkdir_args = {"parents": True, "exist_ok": True}
        if self.file_path.is_dir():
            self.file_path.mkdir(**mkdir_args)
        else:
            self.file_path.parent.mkdir(**mkdir_args)

        default_relative_path = self.default_file_path.relative_to(Path.cwd())
        relative_path = self.file_path.relative_to(Path.cwd())
        shutil.copy2(self.default_file_path, self.file_path)
        print(f"Copied {default_relative_path} to {relative_path}")

        if self._required:
            print(f"{relative_path} requires configuration. Exiting now.")
            sys.exit(1)

    def load(self, exit_on_error=False):
        # Load files in order of default -> local.
        if not self.file_path.exists():
            return

        for config_file in [self.default_file_path, self.file_path]:
            try:
                self.update(yaml.safe_load(config_file.read_text()))
            except TypeError:
                pass
            except yaml.YAMLError as exc:
                print(f"Error loading {config_file.relative_to(Path.cwd())}: {exc}")
                if exit_on_error:
                    sys.exit(1)

        missing_keys = []
        for key in self._required_keys:
            value = self.get(key)
            if value is None or not str(value):
                missing_keys.append(key)

        if not missing_keys:
            return

        relative_path = config_file.relative_to(Path.cwd())
        raise NotConfiguredError(
            f"Required settings are missing in {relative_path}: {missing_keys}"
        )


class LogConfig(YamlConfig):
    def __init__(self, *args, **kwargs):
        super().__init__("logging.yml", *args, **kwargs)


class Config(YamlConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "config.yml",
            required=True,
            *args,
            **kwargs,
        )


class ExtensionConfig(YamlConfig):
    def __init__(self, name, *args, **kwargs):

        super().__init__(
            Path("extensions") / f"{name}.yml",
            *args,
            **kwargs,
        )
