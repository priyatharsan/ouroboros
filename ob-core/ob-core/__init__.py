#built-in libraries
import collections
import functools
import logging

#external libraries
#...

#internal libraries
#...

#exports
__all__ = ('CATELOG',
           'CRITICAL', 'HIGH', 'NORMAL', 'LOW', 'TRIVIAL',
           'coroutine', 'Item', 'PROCESS')

#constants
CATELOG = {}#process catelog

#priorities
CRITICAL = 1
HIGH     = 10
NORMAL   = 100
LOW      = 1000
TRIVIAL  = 10000

EMPTY = {'data': {}, 'ctrl': {}}

Item = collections.namedtuple('Item', ('tag',
                                       'evs', 'args',
                                       'ins', 'reqs',
                                       'outs', 'pros'))

def coroutine(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.next()
        return gen
    return wrapper

def PROCESS(name, level=NORMAL, *items):
    items = {item.tag: item for item in items}
    def decorator(func):
        func = coroutine(func)
        @functools.wraps(func)
        def wrapper(sys, maps, keys):
            try:
                #Pull arguments and events from items
                args = {tag:
                        (lambda tag, names:
                         ((logging.info('data:get:%s', key) or
                           sys[name]['data']
                           [maps[tag]['data'].get(key, key)
                            if maps is not None
                            and tag in maps
                            else key]
                           for key in items[tag].args)
                          for name in names))
                        (tag, names)
                        for tag, names in keys.iteritems()}
                evs = (logging.info('ctrl:get:%s', key) or
                       sys[name]['ctrl']
                       [maps[tag]['ctrl'].get(key, key)
                        if maps is not None
                        and tag in maps
                        else key]
                       for tag, names in keys.iteritems()
                       for name in names
                       for key in items[tag].evs)
                gen = func(**args)#create generator

                evs = yield evs
                while True:
                    #XXX this mess actually calls the function
                    right = {tag:
                             (lambda tag, names:
                              (((logging.info('data:get:%s', key) or
                                 sys[name]['data']
                                 [maps[tag]['data'].get(key, key)
                                  if maps is not None
                                  and tag in maps
                                  else key]
                                 for key in items[tag].reqs),
                                (logging.info('ctrl:get:%s', key) or
                                 sys[name]['ctrl']
                                 [maps[tag]['ctrl'].get(key, key)
                                  if maps is not None
                                  and tag in maps
                                  else key] in evs
                                 for key in items[tag].ins))
                               for name in names))
                             (tag, names)
                             for tag, names in keys.iteritems()}
                    left = gen.send(right)#<---
                    evs = yield (ev for tag, names
                                 in keys.iteritems()
                                 if tag in left
                                 for name, (pros, outs)
                                 in zip(names, left[tag])
                                 for ev in
                                 ((sys[name]['data'].update
                                   ({(maps[tag]['data'].get(key, key)
                                      if maps is not None
                                      and tag in maps
                                      else key):
                                     logging.info('data:set:%s:%s',
                                                  key, pro) or
                                     pro for key, pro
                                     in zip(items[tag].pros, pros)
                                     if pro is not None})) or
                                  (logging.info('ctrl:set:%s:%s',
                                                key, out) or
                                   (sys[name]['ctrl']
                                    [maps[tag]['ctrl'].get(key, key)
                                     if maps is not None
                                     and tag in maps
                                     else key], out) for key, out
                                   in zip(items[tag].outs, outs)
                                   if out is not None))
                                 if pros is not None
                                 and outs is not None)
            except StopIteration:
                return
            finally:
                pass
        CATELOG[name] = (level, wrapper)
        return wrapper
    return decorator