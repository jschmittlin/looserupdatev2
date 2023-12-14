from .settings import Settings, get_default_config
from .load import load_config

_filename = "config.json"


class LooserUpdateV2Configuration(object):
    def __init__(self, settings: Settings = None):
        self._settings = settings

    @property
    def settings(self):
        if self._settings is None:
            config = load_config(_filename)
            settings = Settings(config)
            self._settings = settings
        return self._settings
