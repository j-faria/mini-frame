import numpy as np

class MeanModel(object):
    """ A base class for GP mean functions """
    def __init__(self, *args):
        """ Puts all arguments in an array pars """
        self.pars = np.array(args)

    def __call__(self, t):
        """ t = time """
        raise NotImplementedError

    def __repr__(self):
        """ Representation of each instance """
        return "{0}({1})".format(self.__class__.__name__,
                                 ", ".join(map(str, self.pars)))

class Constant(MeanModel):
    """ A constant offset mean function """
    def __init__(self, c):
        super(Constant, self).__init__(c)
        self.c = c
        
    def __call__(self, t):
        """ Evaluate this mean function at times t """
        t = np.atleast_1d(t)
        return self.c*np.ones_like(t)


class Linear(MeanModel):
    """ 
    A linear mean function
    m(t) = slope * t + intercept 
    """
    def __init__(self, slope, intercept):
        super(Linear, self).__init__(slope, intercept)
        self.slope = slope
        self.intercept = intercept

    def __call__(self, t):
        """ Evaluate this mean function at times t """
        t = np.atleast_1d(t)
        return self.slope * t + self.intercept


class Parabola(MeanModel):
    """ 
    A 2nd degree polynomial mean function
    m(t) = quad * t**2 + slope * t + intercept 
    """
    def __init__(self, quad, slope, intercept):
        super(Parabola, self).__init__(quad, slope, intercept)
        self.quad = quad
        self.slope = slope
        self.intercept = intercept

    def __call__(self, t):
        """ Evaluate this mean function at times t """
        t = np.atleast_1d(t)
        return self.quad * t**2 + self.slope * t + self.intercept


class Keplerian(MeanModel):
    """
    Keplerian function
    tan[phi(t) / 2 ] = sqrt(1+e / 1-e) * tan[E(t) / 2] = true anomaly
    E(t) - e*sin[E(t)] = M(t) = eccentric anomaly
    M(t) = (2*pi*t/tau) + M0 = Mean anomaly

    P  = period in days
    e = eccentricity
    Krv = RV amplitude in m/s 
    w = longitude of the periastron
    T0 = zero phase
    
    RV = Krv[cos(w+v) + e*cos(w)] + sis_vel
    """
    def __init__(self, P, e, Krv, w, T0):
        super(Keplerian, self).__init__(P, e, Krv, w, T0)
        self.P = P
        self.e = e
        self.Krv = Krv
        self.w = w
        self.T0 = T0

    def __call__(self, t):
        """ Evaluate this mean function at times t """
        t = np.atleast_1d(t)
        
        #mean anomaly
        Mean_anom=[2*np.pi*(x1-self.T0)/self.P  for x1 in t]
        #eccentric anomaly -> E0=M + e*sin(M) + 0.5*(e**2)*sin(2*M)
        E0=[x1 + self.e*np.sin(x1)  + 0.5*(self.e**2)*np.sin(2*x1) for x1 in Mean_anom]
        #mean anomaly -> M0=E0 - e*sin(E0)
        M0=[x1 - self.e*np.sin(x1) for x1 in E0]

        i=0
        while i<100:
            #[x + y for x, y in zip(first, second)]
            calc_aux=[x2-y2 for x2,y2 in zip(Mean_anom,M0)]
            E1=[x3 + y3/(1-self.e*np.cos(x3)) for x3,y3 in zip(E0,calc_aux)]
            M1=[x4 - self.e*np.sin(x4) for x4 in E0]
            i+=1
            E0=E1
            M0=M1
        nu=[2*np.arctan(np.sqrt((1+self.e)/(1-self.e))*np.tan(x5/2)) for x5 in E0]
        RV=[self.Krv*(self.e*np.cos(self.w)+np.cos(self.w+x6)) for x6 in nu]
        return RV