#!/usr/bin/env python2.7

"""Messaging service

Author(s):  Sean Henely
Language:   Python 2.x
Modified:   15 September 2014

TBD.

Classes:
MessagingService -- TBD
"""

"""Change log:
                                        
Date          Author          Version     Description
----------    ------------    --------    -----------------------------
2014-06-20    shenely         1.0         Initial revision
2014-09-15    shenely         1.1         No idea what a proxy is

"""


##################
# Import section #
#
#Built-in libraries
import logging

#External libraries
import zmq
from zmq.devices import ThreadDevice

#Internal libraries
from ..device.router import ThreadRouter
from . import ServiceObject
#
##################


##################
# Export section #
#
__all__ = ["MessagingService"]
#
##################


####################
# Constant section #
#
__version__ = "1.1"#current version [major.minor]
#
####################


class MessagingService(ServiceObject):
    
    def __init__(self):
        super(MessagingService,self).__init__()
                
    def start(self):
        if super(MessagingService,self).start():
            self.proxy = ThreadDevice(zmq.FORWARDER, zmq.SUB, zmq.PUB)
            self.router = ThreadRouter()
            
            return True
        else:
            return False
        
    def stop(self):
        if super(MessagingService,self).stop():
            self.proxy.join()
            self.router.join()
            
            return True
        else:
            return False
            
    def pause(self):
        if super(MessagingService,self).pause():
            #XXX:  Can devices really be paused? (shenely, 2014-06-16)
            return True
        else:
            return False
                        
    def resume(self):
        if super(MessagingService,self).resume():
            self.proxy.bind_in("tcp://127.0.0.1:5555")
            self.proxy.bind_out("tcp://127.0.0.1:5556")
            self.router.bind("tcp://127.0.0.1:5560")
            
            self.proxy.setsockopt_in(zmq.SUBSCRIBE,"")
    
            self.run()
            
            return True
        else:
            return False
            
    def run(self):
        if self._running:
            self.proxy.start()
            self.router.start()
        else:
            self.resume()