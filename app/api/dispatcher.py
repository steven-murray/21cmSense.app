#
# dispatcher.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains a simple class for objects that handle json data and optionally
# units.

from abc import abstractmethod


class Dispatcher:
    """The Dispatcher class simplifies the handling of data and unit data in a json object"""

    def __init__(self, data_json, units_json):
        self.data_json = data_json
        self.units_json = units_json

    @abstractmethod
    def get(self, **kwargs):
        pass
