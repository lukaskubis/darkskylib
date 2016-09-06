from builtins import str
from builtins import super

from .slots import *


class Data_point(object):
    __slots__ = data_point_slots

    def __init__(self, data):
        self._data = data
        for name, value in self().items():
            setattr(self, name, value)

    def __call__(self):
        return self._data

    def __setattr__(self, name, value):
        def setvalue(new_val=None):
            return object.__setattr__(self, name, new_val if new_val else value)

        # regular value
        if not isinstance(value, dict) or name == '_data':
            return setvalue()

        # set data handlers
        if name in ['alerts', 'flags']:
            return setvalue(eval(name.capitalize())(value))
        data_block = 'data' in value.keys()
        return setvalue(Data_block(value) if data_block else Data_point(value))

    def __getattr__(self, name):
        if name not in self.__slots__:
            return object.__getattribute__(self, name)


class Data_block(Data_point):
    __slots__ = data_block_slots

    def __call__(self, index=None):
        return self()['data'].__getitem__(index) if index else super().__call__()

    def __setattr__(self, name, value):
        if name == 'data':
            value = [Data_point(data) for data in value]
        return object.__setattr__(self, name, value)

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, index):
        return self.data.__getitem__(index)

    def __len__(self):
        return self.data.__len__()


class Flags(Data_point):
    __slots__ = flags_slots

    def __setattr__(self, name, value):
        name = name.replace('-', '_')
        return object.__setattr__(self, name, value)

    def __str__(self):
        return str(self.raw)


class Alerts(Data_point):
    __slots__ = alerts_slots

    def __str__(self):
        return str(self.raw)
