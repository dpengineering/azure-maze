import os.path
import json
import time
from collections.abc import Mapping


global_config = None

class TraversableDict:
    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, attr):
        if attr in self.obj:
            if isinstance(self.obj[attr], dict):
                return TraversableDict(self.obj[attr])
            else:
                return self.obj[attr]
        raise AttributeError(repr(attr))

class JSONConfig:
    def __init__(self, path, dynamic_reload=False, dynamic_reload_timing=1):
        self.path = os.path.abspath(path)
        self.dynamic_reload = dynamic_reload
        self.dynamic_reload_timing = dynamic_reload_timing
        self.last_reload = None
        self.data = None
        self.reload_config()

    def reload_config(self):
        with open(self.path, "rb") as f:
            res = json.load(f)
        if not isinstance(res, dict):
            raise ValueError("Config root must be a mapping")
        self.data = TraversableDict(res)
        self.last_reload = time.monotonic()

    def should_reload(self):
        return self.dynamic_reload and \
            (time.monotonic() - self.last_reload) >= self.dynamic_reload_timing

    def __getattr__(self, attr):
        if self.should_reload():
            self.reload_config()
        return getattr(self.data, attr)


this_dir = os.path.dirname(os.path.abspath(__file__))
default_config = os.path.join(this_dir, "config.json")
global_config = JSONConfig(default_config)
