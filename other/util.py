import json
import types
import functools
from datetime import timedelta

from bson import json_util
from numpy import ndarray,array

__all__ = ["coroutine",
           "Go", "All", "Many", "One", "No",
           "dumps", "loads"]

def coroutine(func):
    def wrapper(*args,**kwargs):
        gen = func(*args,**kwargs)
        gen.next()
        return gen
    
    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__  = func.__doc__
    
    return wrapper

class Go(Exception):pass

class All(Go):pass

class Many(Go):

    def __init__(self,*outs):
        self.value = outs

class One(Go):

    def __init__(self,out):
        self.value = out

class No(Go):pass

def object_hook(dct):
    dct = json_util.object_hook(dct)

    if isinstance(dct,types.DictType):
        if "$elapse" in dct:
            dct = timedelta(dct["$elapse"])
        elif "$array" in dct:
            dct = array(dct["$array"])

    return dct

def default(obj):
    if isinstance(obj,timedelta):
        obj = { "$elapse": obj.total_seconds() }
    elif isinstance(obj,ndarray):
        obj = { "$array": obj.tolist() }
    else:
        obj = json_util.default(obj)

    return obj

dumps = functools.partial(json.dumps,default=default)
loads = functools.partial(json.loads,object_hook=object_hook)