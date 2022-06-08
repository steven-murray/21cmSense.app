#
# models.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains various utility functions

import numpy

def get_unit_string(obj_with_unit):
    return obj_with_unit.unit.to_string()



def filter_infinity(list1: list, list2: list):
    """remove ungraphable infinity values in two parallel lists

        list1[n] is infty OR list2[n] is infty -> list1[n] and list2[n] will both be removed

    Parameters
    ----------
    list1
        first list
    list2
        second list

    Returns
    -------
    tuple
        ( newlist1, newlist2 )

    """
    return zip(*(filter(lambda t: t[0] != numpy.inf and t[1] != numpy.inf, zip(list1, list2))))


def quantity_list_to_scalar(lst: list):
    """convert all AstroPy 'quantity' objects to scalars and return new list

    Parameters
    ----------
    l
        input list of Astropy 'quantity' objects

    Returns
    -------
    list
        list of scalars

    """
    return [t.value for t in lst]
