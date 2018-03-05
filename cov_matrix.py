# -*- coding: utf-8 -*-
import kernels
import numpy as np

def build_smallmatrix(kernel, x):
    """
        build_smallmatrix() creates the smaller covariance matrices,
    equations 18 to 23 in the paper.
        
        Parameters
    kernel = kernel in use
    x = range of values of the independent variable (usually time)
    y = range of values of te dependent variable (the measurments)
    yerr = error in the measurments
    
        Returns
    K = covariance matrix
    """ 
    r = x[:, None] - x[None, :]
    K = kernel(r)

    return K


def k11(kern, a, x):
    """
        Equation 18
    """
    if kern == 1:
        l,vc,vr,lc,bc,br = a        
        gammagg  = build_smallmatrix(kernels.SquaredExponential(l),x) 
        gammadgdg = build_smallmatrix(kernels.ddSE_dt2dt1(l),x)  
        gammagdg = build_smallmatrix(kernels.dSE_dt1(l),x)  
        gammadgg = build_smallmatrix(kernels.dSE_dt2(l),x)  
    
    if kern == 2:
        lp,le,p,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.QuasiPeriodic(lp,le,p),x) 
        gammadgdg = build_smallmatrix(kernels.ddQP_dt2dt1(lp,le,p),x)  
        gammagdg = build_smallmatrix(kernels.dQP_dt1(lp,le,p),x)  
        gammadgg = build_smallmatrix(kernels.dQP_dt2(lp,le,p),x) 
        
    return vc**2 * gammagg + vr**2* gammadgdg + vc*vr*(gammagdg + gammadgg)
    
def k22(kern, a, x):
    """
        Equation 19
    """
    if kern == 1:
        l,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.SquaredExponential(l),x)

    if kern == 2:
        lp,le,p,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.QuasiPeriodic(lp,le,p),x)

    return lc**2 * gammagg

def k33(kern, a, x):
    """
        Equation 20
    """
    if kern == 1:
        l,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.SquaredExponential(l),x) 
        gammadgdg = build_smallmatrix(kernels.ddSE_dt2dt1(l),x)  
        gammagdg = build_smallmatrix(kernels.dSE_dt1(l),x)  
        gammadgg = build_smallmatrix(kernels.dSE_dt2(l),x)  
        
    if kern == 2:
        lp,le,p,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.QuasiPeriodic(lp,le,p),x) 
        gammadgdg = build_smallmatrix(kernels.ddQP_dt2dt1(lp,le,p),x)  
        gammagdg = build_smallmatrix(kernels.dQP_dt1(lp,le,p),x)  
        gammadgg = build_smallmatrix(kernels.dQP_dt2(lp,le,p),x)  

    return bc**2 * gammagg + br**2* gammadgdg + bc*br*(gammagdg + gammadgg)

def k12(kern, a, x):
    """
        Equation 21
    """
    if kern == 1:
        l,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.SquaredExponential(l),x) 
        gammagdg = build_smallmatrix(kernels.dSE_dt1(l),x)  

    if kern == 2:
        lp,le,p,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.QuasiPeriodic(lp,le,p),x) 
        gammagdg = build_smallmatrix(kernels.dQP_dt1(lp,le,p),x) 
    
    return vc*lc * gammagg + vr*lc*gammagdg

def k13(kern, a, x):
    """
        Equation 22
    """
    if kern == 1:    
        l,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.SquaredExponential(l),x) 
        gammadgdg = build_smallmatrix(kernels.ddSE_dt2dt1(l),x)  
        gammagdg = build_smallmatrix(kernels.dSE_dt1(l),x)  
        gammadgg = build_smallmatrix(kernels.dSE_dt2(l),x)  
        
    if kern == 2:
        lp,le,p,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.QuasiPeriodic(lp,le,p),x) 
        gammadgdg = build_smallmatrix(kernels.ddQP_dt2dt1(lp,le,p),x)  
        gammagdg = build_smallmatrix(kernels.dQP_dt1(lp,le,p),x)  
        gammadgg = build_smallmatrix(kernels.dQP_dt2(lp,le,p),x) 

    return vc*bc*gammagg + vr*br* gammadgdg + vc*br*gammagdg + vr*bc*gammadgg


def k23(kern, a, x):
    """
        Equation 23
    """
    if kern == 1:
        l,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.SquaredExponential(l),x) 
        gammagdg = build_smallmatrix(kernels.dSE_dt1(l),x)  
    
    if kern == 2:
        lp,le,p,vc,vr,lc,bc,br = a
        gammagg  = build_smallmatrix(kernels.QuasiPeriodic(lp,le,p),x) 
        gammagdg = build_smallmatrix(kernels.dQP_dt1(lp,le,p),x)  

    return bc*lc * gammagg + br*lc*gammagdg
        
def build_bigmatrix(kern, a, x, y, yerr):
    """
        build_bigmatrix() creates the big covariance matrix,
    equations 24 in the paper.
        
        Parameters
    kern = kernel being used: 
            1 for squared exponential
            2 for quasi periodic
    a = array with the important parameters
    x = range of values of the independent variable (usually time)
    y = range of values of te dependent variable (the measurments)
    yerr = error in the measurments
    
        Returns
    K = covariance matrix
    """ 
    listofkerns = [1, 2]
    if not kern in listofkerns:    
        print('Invalid kernel value!')
        print('Choose: \n 1 for squared exponential \n 2 for quasi periodic')
        print
        raise SystemExit
        
    K11 = k11(kern,a,x)
    K22 = k22(kern,a,x)
    K33 = k33(kern,a,x)
    K12 = k12(kern,a,x)
    K13 = k13(kern,a,x)
    K23 = k23(kern,a,x)
    
    K1 = np.hstack((K11,K12,K13))
    K2 = np.hstack((K12,K22,K23))
    K3 = np.hstack((K13,K23,K33))
    
    K = np.vstack((K1,K2,K3))
    K = K + yerr**2*np.identity(len(yerr))

    return K