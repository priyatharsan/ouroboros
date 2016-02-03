from math import sqrt
from datetime import datetime,timedelta

from numpy import array

from core import System
from orbit import *
from coord import *
import web

EARTH_RADIUS = 6378.1
EARTH_FLATTENING = 0.00335
EARTH_GRAVITATION = 398600.4

J2000 = datetime(2000,1,1,12)#Julian epoch (2000-01-01T12:00:00Z)

SECOND = timedelta(seconds=1)
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

#Unit vectors
O = array([0,0,0])
I = array([1,0,0])
J = array([0,1,0])
K = array([0,0,1])

def main():
    web.main()

    sys = System(t_dt=J2000,
                 dt_td=MINUTE)
    sys.init("earth",
             r_bar=O,
             th_G=100.4606184,
             mu=EARTH_GRAVITATION,
             f=EARTH_FLATTENING,
             R_km=EARTH_RADIUS)
    sys.init("gs",lat_deg=60,lon_deg=-60,alt_m=100)
    sys.init("sc",r_bar=sqrt(2)*7000.0/2*(I+K),v_bar=7.4*J)

    sys.every(1,until=3600)
    sys.every(5,until=3600)

    clock(sys, None)
    earth(sys, None, "earth")
    orbit(sys, None,"sc", "earth")
    #nrt2fix(sys, "earth", "sc", ("earth", "sc"))
    #fix2geo(sys, "earth", ("earth", "sc"))

    sys.run()
    
if __name__ == "__main__":
    main()