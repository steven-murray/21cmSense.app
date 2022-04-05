from abc import abstractmethod


class Dispatcher:
    """The Dispatcher class simplifies the handling of data and unit data in a json object

    """

    def __init__(self, data_json, units_json):
        self.data_json = data_json
        self.units_json = units_json

    @abstractmethod
    def get(self, **kwargs):
        pass
