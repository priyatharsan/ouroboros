from numpy import hstack, hsplit
from scipy.integrate import ode

from core import Process
from util import O

__all__= ["model",
          "quat2rec", "rec2quat",
          "quat2rpy", "rpy2quat",
          "quat2mat", "mat2quat"]

KILO = 1000
MICRO = 1e-6

@Process((["t_dt"], ["+1*"], [], ["t_dt"], []),
         (["_bar", "_t_bar"], [], ["rec"], [], ["_bar", "_t_bar"]))
def model(t0_dt, th0_bar, om0_bar):
    def rigid(t,y):
        th_bar, om_bar = hsplit(y, 2)
        
        dy = hstack((om_bar, O))
        
        return dy
    
    y = hstack((th0_bar,om0_bar))
    
    box = ode(rigid)\
            .set_integrator("dopri5") \
            .set_initial_value(y, 0)
    
    th_bar, om_bar = th0_bar, om0_bar
    
    while True:
        #Input/output
        t_dt, = yield th_bar, om_bar,#time/position,velocity
        
        #Update state
        y = box.integrate((t_dt - t0_dt).total_seconds())
        th_bar, om_bar = hsplit(y, 2)

def quat2rec():pass
def rec2quat():pass
def quat2rpy():pass
def rpy2quat():pass
def quat2mat():pass
def mat2quat():pass