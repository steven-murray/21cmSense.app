from .factorymanager import FactoryManager
from .dispatcher import Dispatcher
from py21cmsense import Observatory

class ObservatoryFactory(FactoryManager):
    def __init__(self):
        super().__init__("observatory")

    class _observatory(Dispatcher):

        # needs antenna position array, beam object, latitude float
        def get(self, antpos, beam, latitude):

            j = self.data_json
            u = self.units_json

            return Observatory(antpos=antpos, beam=beam, latitude=latitude)
