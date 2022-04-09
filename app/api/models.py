#
# models.py
#


from py21cmsense import GaussianBeam, Observation, Observatory, PowerSpectrum, hera
from astropy import units
# from .calculation import CalculationFactory
from .constants import *
from .exceptions import CalculationException
from .factorymanager import FactoryManager
from .dispatcher import Dispatcher
from .redisfuncs import get_antpos_json
from .util import DebugPrint

debug = DebugPrint(0).debug_print


class LocationFactory(FactoryManager):
    def __init__(self):
        super().__init__("location")
        # self.add('latitude', LatitudeDispatcher)

    class _latitude(Dispatcher):
        """Handles latitude

        """

        def get(self):
            return self.data_json['latitude'] * units.Unit(self.units_json['latitude'])


class BeamFactory(FactoryManager):
    def __init__(self):
        super().__init__("beam")
        # self.add('GaussianBeam', GaussianBeamDispatcher).add('FakeBeam', GaussianBeamDispatcher)

    class _GaussianBeam(Dispatcher):
        """
        Makes a py21cmSense library call to the GaussianBeam class
        """

        def get(self):
            # TODO - add error checking on units
            # return GaussianBeam(frequency=self.data_json['frequency'] * units.Unit("MHz"),
            #                     dish_size=self.data_json['dish_size'] * units.Unit("m"))
            return GaussianBeam(frequency=self.data_json['frequency'] * units.Unit(self.units_json['frequency']),
                                dish_size=self.data_json['dish_size'] * units.Unit(self.units_json['dish_size']))


class AntennaFactory(FactoryManager):
    def __init__(self):
        super().__init__("antenna")
        # self.add('ahera', HeraAntennaDispatcher)
        # print("ANTENNA DICT=",self.d)

    # uses stored antenna position data stored in redis database
    class _custom(Dispatcher):
        """Allows the use of user-supplied antenna position data
        """

        # exceptions bubble up to be handled in sensitivity.py
        def get(self):

            # remember data_json IS the _data_ json for the _antenna_ object, so we don't
            # have to look deep into the json; it's already here!
            objid = self.data_json['id']
            (name, data) = get_antpos_json(objid)

            if name is None:
                raise CalculationException("No stored antenna data with provided ID")

            data=data*units.Unit("m")

            return data




    class _hera(Dispatcher):
        """makes a py21cmSense call to the hera antenna class
        """

        def get(self):
            j = self.data_json
            u = self.units_json

            # TODO - error checking on units
            # return hera(hex_num=j['hex_num'], separation=j['separation'] * units.Unit("m"),
            #             dl=j['separation'] * units.Unit("m"))

            return hera(hex_num=j['hex_num'], separation=j['separation'] * units.Unit(u['separation']),
                        dl=j['dl'] * units.Unit(u['dl']))
