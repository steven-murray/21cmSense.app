import py21cmsense
import attr
import sys
import inspect
from py21cmsense import *
from py21cmsense.beam import PrimaryBeam
from py21cmsense.sensitivity import Sensitivity

objs = dir(py21cmsense)

base_classes = [PrimaryBeam]
# target_classes = [Observation, Observatory, Sensitivity]
target_classes = []

# for o in objs:
#     print("Got obj=", o)
#
# print(globals())

for el in inspect.getmembers(py21cmsense):
    cls = el[1]
    if inspect.isclass(cls):
        for sup in base_classes:
            if issubclass(cls, sup):
                target_classes.append(cls)

for cls in target_classes:
    print("Target class: ", cls)

    a = attr.fields(cls)
    # print("attrs for " + el[0] + " are ", a)
    for at in a:
        print("Got attr: ", at.name, ", default=", "" if inspect.isclass(at.default) else at.default)
# else:
#     print("Not class: ", el[0])

sys.exit(1)

# for o in objs:
#     obj=globals()[o]
#     if not '__' in o and attr.has(obj):
#         a=attr.fields(globals()[obj])
#         print("attrs for "+o+" are ",a)
