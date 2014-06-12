#!/usr/bin/env python2.7

"""Routine behaviors

Author(s):  Sean Henely
Language:   Python 2.x
Modified:   11 June 2014

TBD.

Classes:
SourceBehavior    -- TBD
TargetBehavior    -- TBD
EventBehavior     -- TBD
ActionBehavior    -- TBD
ConditionBehavior -- TBD
"""

"""Change log:
                                        
Date          Author          Version     Description
----------    ------------    --------    -----------------------------
2014-05-06    shenely         1.0         Initial revision
2014-06-11    shenely                     Added documentation

"""


##################
# Import section #
#
#Built-in libraries
import logging

#External libraries

#Internal libraries
from behavior import PrimitiveBehavior
#
##################=


##################
# Export section #
#
__all__ = ["SourceBehavior",
           "TargetBehavior",
           "EventBehavior",
           "ActionBehavior",
           "ConditionBehavior"]
#
##################


####################
# Constant section #
#
__version__ = "1.0"#current version [major.minor]
# 
####################


class SourceBehavior(PrimitiveBehavior):
    """Source primitive (for use with 'to' clause)'"""
    
    def _process(self):
        logging.debug("{0}:  Receiving".\
                     format(self.name))
        
        message = self._receive()
        
        self.set("message",message)
        
        logging.debug("{0}:  Received".\
                     format(self.name))
        
        return Ellipsis
    
    def _receive(self):
        raise NotImplemented

class TargetBehavior(PrimitiveBehavior):
    """Target primitive (for use with 'to' clause)'"""
    
    def _process(self):
        logging.debug("{0}:  Sending".\
                     format(self.name))
        
        message = self.get("message")
        
        self._send(message)
        
        logging.debug("{0}:  Sent".\
                     format(self.name))
        
        return Ellipsis
    
    def _send(self,message):
        raise NotImplemented
    
class EventBehavior(PrimitiveBehavior):
    """Event primitive (for use with 'when' clause)'"""
    
    def _process(self):
        logging.debug("{0}:  Occurring".\
                      format(self.name))
        
        mode = self._occur()
        
        if mode is not None:
            logging.debug("{0}:  Occurred".\
                         format(self.name))
        else:
            logging.warn("{0}:  False alarm".\
                         format(self.name))
            
        return mode
    
    def _occur(self):
        raise NotImplemented
    
class ActionBehavior(PrimitiveBehavior):
    """Action primitive (for use with 'then' clause)'"""
    
    def _process(self):
        logging.debug("{0}:  Executing".\
                      format(self.name))
        
        self._execute()
        
        logging.debug("{0}:  Executed".\
                     format(self.name))
            
        return Ellipsis
    
    def _execute(self):
        raise NotImplemented
    
class ConditionBehavior(PrimitiveBehavior):
    """Condition primitive (for use with 'given' clause)'"""
    
    def _process(self):
        logging.debug("{0}:  Satisfying".\
                      format(self.name))
            
        if self._satisfy():
            logging.debug("{0}:  Satisfied".\
                          format(self.name))
            
            mode = True
        else:
            logging.warning("{0}:  Not satisfied".\
                         format(self.name))
            
            mode = False
            
        return mode
    
    def _satisfy(self,message):
        raise NotImplemented
        