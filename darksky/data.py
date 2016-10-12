from builtins import str
from builtins import super


class Data_point(object):
    def __init__(self, data):
        self._data = data

        if isinstance(self(), dict):
            for name, val in self().items():
                setattr(self, name, val)

        if isinstance(self(), list):
            setattr(self, 'data', self())

    def __call__(self):
        return self._data

    def __setattr__(self, name, val):
        def setval(new_val=None):
            return object.__setattr__(self, name, new_val if new_val else val)

        # regular value
        if not isinstance(val, (list, dict)) or name == '_data':
            return setval()

        # set specific data handlers
        if name in ('alerts', 'flags'):
            return setval(eval(name.capitalize())(val))

        # data
        if isinstance(val, list):
            val = [Data_point(v) if isinstance(v, dict) else v for v in val]
            return setval(val)

        # set general data handlers
        setval(Data_block(val) if 'data' in val.keys() else Data_point(val))

    def __getattr__(self, name):
        return


class Data_block(Data_point):
    def __call__(self, index=None):
        return self.__getitem__(index)() if index is not None else self._data

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, index):
        return self.data.__getitem__(index)

    def __len__(self):
        return self.data.__len__()


class Flags(Data_point):
    def __setattr__(self, name, value):
        return object.__setattr__(self, name.replace('-', '_'), value)


class Alerts(Data_block):
    pass
