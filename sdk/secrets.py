import os

from pipedrive.settings.base import BaseSettings
from pipedrive.settings.master import MasterSettings
from pipedrive.settings.test import TestSettings


env_name = os.environ.get("DJANGO_SETTINGS_MODULE", "settings.settings.local")
print("ENVIRON ", env_name)

class_settings = {
    "settings.settings.test": TestSettings,
    "settings.settings.local": TestSettings,
    "settings.settings.dev": TestSettings,
    "settings.settings.staging": TestSettings,
    "settings.settings.ci_test": TestSettings,
    "settings.settings.master": MasterSettings,
}

settings: BaseSettings = class_settings[env_name]
