'''
Created on Jan 28, 2016

@author: weiluo
'''

from dm_expXdrift import DM_expXdrift
from run_dm_iteration_helpers import dm_iterate_then_pickle


class DM_linearizedXdrift(DM_expXdrift):
    '''
    dQ_t = [A(1 - \kappa \Delta^b_t) - A( 1- \kappa \Delta^a_t)] dt + \sigma dB_t
    dY_t = -2 \beta * EY_0 * e^{-2\beta t} dt + Z_t dB_t
    Q_0 = q_0; Y_T = -2m Q_T
    where \Delta^b_t = 1 / \kappa - Y_t; \Delta^a_t = 1 / \kappa + Y_t
    
    ==>
    
    dX_t = 2A\kappa Y_t dt + \sigma dW_t
    dY_t = -2 \beta * x * e^{-2\beta t} dt + Z_t dW_t
    X_0 = x_0, Y_T = -2m * X_T
    
    We want to compute the distribution of
    Y_0
    '''


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def F(self, x, y):
        return 2 * self.A * self.kappa * y
        
        
class DM_linearizedXdrift_linearYdrift(DM_linearizedXdrift):
    '''
    dQ_t = [A(1 - \kappa \Delta^b_t) - A( 1- \kappa \Delta^a_t)] dt + \sigma dB_t
    dY_t = -2 \beta * Y_t dt + Z_t dB_t
    Q_0 = q_0; Y_T = -2m Q_T
    where \Delta^b_t = 1 / \kappa - Y_t; \Delta^a_t = 1 / \kappa + Y_t
    
    ==>
    
    dX_t = 2A\kappa Y_t dt + \sigma dW_t
    dY_t = -2 \beta * Y_t dt + Z_t dW_t
    X_0 = x_0, Y_T = -2m * X_T
    
    We want to compute the distribution of
    Y_0
    '''


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def G(self, time_index, y):
        return -2 * self.beta * y
    
    
class DM_linearizedXdrift_linearYdrift_useExpectationOnYdrift(DM_linearizedXdrift):
    '''
    dX_t = 2A\kappa Y_t dt + \sigma dW_t
    dY_t = -2 \beta * Y_t dt + Z_t dW_t
    X_0 = x_0, Y_T = -2m * X_T
    
    We want to compute the distribution of
    Y_t
    '''


    def __init__(self, eta, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eta = eta
        
    def G(self, time_index, y):
        return -2 * self.beta * self.eta[time_index]


def linearizdeXdrift_linearYdrift_factory(phase, *args, **kwargs):
    if phase == 'init':
        return DM_linearizedXdrift_linearYdrift(*args, **kwargs)
    elif phase == 'use_expectation':
        return DM_linearizedXdrift_linearYdrift_useExpectationOnYdrift(*args, **kwargs)
    else:
        raise Exception("phase should be " +
                         "either 'init' for the starting phase " +
                         "or 'use_expectation' for the following phase")
   
    
def dm_iterate_then_pickle_linearizedXdrift_linearYdrift(file_name, *args, **kwargs):
    return dm_iterate_then_pickle(linearizdeXdrift_linearYdrift_factory,
                                  file_name,
                                  *args, **kwargs)
    