# data.py

class Data_point(object):
    def __init__(self, data):
        self.rawdata = data

        if isinstance(self.rawdata, dict):
            for name, val in self.rawdata.items():
                setattr(self, name, val)

        if isinstance(self.rawdata, list):
            setattr(self, 'data', self.rawdata)

    def __setattr__(self, name, val):
        def setval(new_val=None):
            return object.__setattr__(self, name, new_val if new_val else val)

        # regular value
        if not isinstance(val, (list, dict)) or name == 'rawdata':
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
