import numpy
import csv


class DebugPrint:
    level = 0

    def __init__(self, level: int = 0):
        DebugPrint.level = level

    def set_level(self, level: int):
        DebugPrint.level = level

    def get_level(self):
        return DebugPrint.level

    def debug_print(self, msg, debug_level: int = 3):
        if 0 < debug_level <= self.get_level():
            print("DEBUG(", debug_level, "): " + msg, sep="")



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


def quantity_list_to_scalar(l: list):
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
    newl = []
    for t in l:
        newl.append(t.value)
    return newl


def import_csv(csv: str)-> dict:

    pass
