# data.py


class DataPoint(object):
    def __init__(self, data):
        self._data = data

        if isinstance(self._data, dict):
            for name, val in self._data.items():
                setattr(self, name, val)

        if isinstance(self._data, list):
            setattr(self, 'data', self._data)

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
            val = [DataPoint(v) if isinstance(v, dict) else v for v in val]
            return setval(val)

        # set general data handlers
        setval(DataBlock(val) if 'data' in val.keys() else DataPoint(val))

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)


class DataBlock(DataPoint):
    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, index):
        # keys in darksky API datablocks are always str
        if isinstance(index, str):
            return self._data[index]
        return self.data.__getitem__(index)

    def __len__(self):
        return self.data.__len__()


class Flags(DataPoint):
    def __setattr__(self, name, value):
        return object.__setattr__(self, name.replace('-', '_'), value)


class Alerts(DataBlock):
    pass
