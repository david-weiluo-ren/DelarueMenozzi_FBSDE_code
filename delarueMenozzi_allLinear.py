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

class DelarueMenozzi_allLinear(DelarueMenozziSimplifiedCaseBase):
    '''
    dX_t = -Y_t dt + \sigma dW_t
    dY_t = K Y_t dt + Z_t dW_t
    X_0 = x_0, Y_T = m X_T
    
    We want to compute the distribution of
    Y_t from 0 to T.
    
    '''

    def __init__(self, K = 1,  m = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.K = K
        self.m = m
    
    def F(self, time_index, x, y):
        return -1 * y
    def G(self, time_index, y):
        return self.K * y
    def f(self, x):
        return self.m * x
    def g(self, y):
        return y
    
       
class DelarueMenozzi_allLinear_useExpectationOnYdrift(DelarueMenozzi_allLinear):
    '''
    dX_t = -Y_t dt + \sigma dW_t
    dY_t = K * eta_t dt + Z_t dW_t
    X_0 = x_0, Y_T = m X_T
    
    eta_t comes from the previoous iteration
    
    We want to compute the distribution of
    Y_t
    
    '''


    def __init__(self, eta, *args, **kwargs):
        self.eta = list(eta) 
        super().__init__(*args, **kwargs)
        
    def G(self, time_index, y):
        return self.K * self.eta[time_index]
        
def allLinear_factory(phase, *args, **kwargs):
    if phase == 'init':
        return DelarueMenozzi_allLinear(*args, **kwargs)
    elif phase == 'use_expectation':
        return DelarueMenozzi_allLinear_useExpectationOnYdrift(*args, **kwargs)
    else:
        raise Exception("phase should be " +
                         "either 'init' for the starting phase " +
                         "or 'use_expectation' for the following phase")
def iterate_allLinear(iter_number = 20, *args, **kwargs):
    return dm_iterate_helper(allLinear_factory, iter_number, *args, **kwargs)


def dm_iterate_then_pickle_allLinear(file_name, *args, **kwargs):
    return dm_iterate_then_pickle(allLinear_factory, file_name, *args, **kwargs)
    
    
    
    
    
    