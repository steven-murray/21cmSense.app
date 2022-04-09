#
# observatory.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains support for optional observatory data.
# This functionality has not been implemented in the front end and is a WIP

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
