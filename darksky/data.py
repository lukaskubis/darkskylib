from builtins import str
from builtins import super


class Data_point(object):
    def __init__(self, data):
        self._data = data
        for name, val in self().items():
            setattr(self, name, val)

    def __call__(self):
        return self._data

    def __setattr__(self, name, val):
        def setval(new_val=None):
            return object.__setattr__(self, name, new_val if new_val else val)

        # regular value
        if not isinstance(val, dict) or name == '_data':
            return setval()

        # set specific data handlers
        if name in ['alerts', 'flags']:
            return setval(eval(name.capitalize())(val))

        # set general data handlers
        setval(Data_block(val) if 'data' in val.keys() else Data_point(val))

    def __getattr__(self, name):
        if name not in self.__slots__:
            return object.__getattribute__(self, name)


class Data_block(Data_point):
    def __call__(self, index=None):
        return self.__getitem__(index) if index else super().__call__()

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
    def __setattr__(self, name, value):
        name = name.replace('-', '_')
        return object.__setattr__(self, name, value)

    def __str__(self):
        return str(self())


class Alerts(Data_point):
    def __str__(self):
        return str(self())
