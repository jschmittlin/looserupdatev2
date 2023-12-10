try:
    import ujson as json
except ImportError:
    import json


class DtoObject(dict):
    @property
    def __dict__(self):
        return {k: v for k, v in self.items()}

    def to_json(self, **kwargs):
        return json.dumps(self, **kwargs)
