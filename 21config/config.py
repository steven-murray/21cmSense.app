import py21cmsense
import attr
import sys
import inspect

objs = dir(py21cmsense)

for o in objs:
    print("Got obj=", o)

print(globals())

for el in inspect.getmembers(py21cmsense):
    if inspect.isclass(el[1]):
        print("Found class: ", el[0])
        a = attr.fields(el[1])
        # print("attrs for " + el[0] + " are ", a)
        for at in a:
            print("Got attr: ", at.name,", default=","" if inspect.isclass(at.default) else at.default)
    # else:
    #     print("Not class: ", el[0])

sys.exit(1)

# for o in objs:
#     obj=globals()[o]
#     if not '__' in o and attr.has(obj):
#         a=attr.fields(globals()[obj])
#         print("attrs for "+o+" are ",a)
