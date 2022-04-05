from .factorymanager import FactoryManager
from .dispatcher import Dispatcher
from py21cmsense import Observation

class ObservationFactory(FactoryManager):
    def __init__(self):
        super().__init__("observation")

    class _observation(Dispatcher):
        def get(self, **kwargs):
            j = self.data_json
            u = self.units_json

            return Observation()

