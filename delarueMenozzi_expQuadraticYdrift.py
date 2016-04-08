'''
Created on Jan 27, 2016

@author: weiluo
'''
from importlib import reload
import delarueMenozzi_simplifedCase_base
reload(delarueMenozzi_simplifedCase_base)

from delarueMenozzi_simplifedCase_base import DelarueMenozziSimplifiedCaseBase
from run_dm_iteration_helpers import dm_iterate_helper, dm_iterate_then_pickle

import numpy as np

class DelarueMenozzi_expQuadraticYdrift(DelarueMenozziSimplifiedCaseBase):
    '''
    dX_t = -Y_t dt + \sigma dW_t
    dY_t = A * e^{- \kappa Y_t^2} dt + Z_t dW_t
    X_0 = x_0, Y_T = m X_T
    
    We want to compute the distribution of
    g(Y_t) from 0 to T.
    g = A * e^{- \kappa^2 Y_t}
    '''

    def __init__(self, A = 1, kappa = 1, m = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.A = A
        self.kappa = kappa
        self.m = m
    
    def F(self, time_index, x, y):
        return -1 * y
    def G(self, time_index, y):
        return self.g_G_helper(time_index, y)
    def f(self, x):
        return self.m * x
    def g(self, y):
        return self.g_G_helper(0, y)
    
    def g_G_helper(self, time_index, y):
        return self.A * np.exp(-1 * self.kappa * (y ** 2))
    
    
    
class DelarueMenozzi_expQuadraticYdrift_useExpectationOnYdrift(DelarueMenozzi_expQuadraticYdrift):
    '''
    dX_t = -Y_t dt + \sigma dW_t
    dY_t = eta_t dt + Z_t dW_t
    X_0 = x_0, Y_T = m X_T
    
    eta_t comes from the previoous iteration
    
    We want to compute the distribution of
    g(Y_t) from 0 to T.
    g = A * e^{- \kappa^2 Y_t}
    '''


    def __init__(self, eta, *args, **kwargs):
        self.eta = list(eta) 
        super().__init__(*args, **kwargs)
        
    def G(self, time_index, y):
        return self.eta[time_index]
        
def expQuadratic_factory(phase, *args, **kwargs):
    if phase == 'init':
        return DelarueMenozzi_expQuadraticYdrift(*args, **kwargs)
    elif phase == 'use_expectation':
        return DelarueMenozzi_expQuadraticYdrift_useExpectationOnYdrift(*args, **kwargs)
    else:
        raise Exception("phase should be " +
                         "either 'init' for the starting phase " +
                         "or 'use_expectation' for the following phase")
def iterate_expQuadraticYdrift(iter_number = 20, *args, **kwargs):
    return dm_iterate_helper(expQuadratic_factory, iter_number, *args, **kwargs)


def dm_iterate_then_pickle_expQuadraticYdrift(file_name, *args, **kwargs):
    return dm_iterate_then_pickle(expQuadratic_factory, file_name, *args, **kwargs)
    
    
    
    
    
    