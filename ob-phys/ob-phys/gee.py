# built-in libraries
# ...

# external libraries
import scipy.linalg

# internal libraries
from ouroboros import Type, Image, Node
from ouroboros.lib import libkin

# exports
__all__ = ("kin",
           "point")

# constants
GRAVITY_CONST = 6.67808e-11

kin = Type(".gee#kin", libkin.kin,
           libkin.kin._asdict,
           lambda x: libkin.kin(**x))

@Image(".gee@point",
       one=Node(evs=(), args=("m",),
                ins=(), reqs=(),
                outs=(), pros=()),
       two=Node(evs=(), args=("m",),
                ins=(), reqs=(),
                outs=(), pros=()),
       fun=Node(evs=("i",), args=(),
                ins=(), reqs=("t", "y"),
                outs=("o",), pros=("y_dot",)))
def point(env, clk, bod, orb):
    """Point gravity"""
    m1, = next(one.data)
    m2, = next(two.data)
    mu = GRAVITY_CONST * m1 * m2  # m3/kg/s2

    yield
    while True:
        t, y = next(fun.data)
        
        (r, v) = y
        r_dot = v
        v_dot = - mu * r / scipy.linalg.norm(r) ** 3
        y_dot = libkin.kin(r_dot, v_dot)
        
        fun.data.send((y_dot,))
        yield (fun.ctrl.send((False,)),)
