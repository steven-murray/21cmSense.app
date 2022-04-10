#
# createSchema.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains prototype code for automatic schema creation

import types

import py21cmsense
import inspect
import typing
from typing import Optional
from typing import Annotated
from typing import get_args
from typing import get_origin
from inspect import get_annotations

sources = {'antenna': 'antpos'}

print("Select a source")
l = list(sources)
for i in range(len(l)):
    print(i, ": " + l[i])

s = input()
if s.isnumeric():
    print("s numeric")

for k in sources:
    print("Select")
print("Enter name of function to support: ")
dir(py21cmsense)

print("checking members")

mod = "py21cmsense" + "." + sources['antenna']

z = inspect.getmembers(mod, lambda x: isinstance(x, types.FunctionType))
print("Select a function to import into json:")
for m in z:
    print("m[0]=", m[0], "; m[1]=", m[1], "; type(m[1])=", type(m[1]))

fn = 'hera'

fullfn = mod + "." + fn

# new in python 3.10

# really no point to this because we need all parameters (gotten with inspect.signature.parameters)
# - not just annotated parameters
aa = get_annotations(eval(fullfn))
print("get_annotations returns ", aa)

# sig is a Signature object
sig = inspect.signature(py21cmsense.hera)
ret = sig.return_annotation
parms = sig.parameters

print("ret=", ret)
print("parms=", parms)

i = 0
for k in parms:
    p = parms[k]
    print("arg ", i, ": ", k, " has type: ", p)

    # this is a Parameter type
    # See if it has an annotation
    if p.default is p.empty:
        print("No annotation on this parameter")
    else:
        # get its annotation
        a = p.annotation

        print("annotation is ", a)

        # see if it's optional
        # sadly, there's not a great way to see if something is typing.Optional.
        # if a is typing.Optional: # doesn't work - decomposes to a mess
        if get_origin(a) == typing.Union and type(None) in get_args(a):
            # opt_value = a.__args__[0]
            print("got optional value of ", get_args(a))
            a = get_args(a)[0]
            print("canonical annotation is ", a)

    # a = parms[p].annotation

    # print("annotation=",a)

    # if a.instanceOf(Optional):
    #     print("Got optional on ", p)
    #     print(a.__args__[0])
    i = i + 1
