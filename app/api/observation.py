#
# observation.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains support for optional observation data.
# this functionality is not supported by the front end and is a WIP

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

