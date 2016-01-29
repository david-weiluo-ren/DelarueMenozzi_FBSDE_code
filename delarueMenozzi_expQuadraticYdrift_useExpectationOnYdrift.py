'''
Created on Jan 27, 2016

@author: weiluo
'''

from importlib import reload
import delarueMenozzi_expQuadraticYdrift
reload(delarueMenozzi_expQuadraticYdrift)

from delarueMenozzi_expQuadraticYdrift import DelarueMenozzi_expQuadraticYdrift
from run_dm_iteration_helpers import dm_iterate_helper

class DelarueMenozzi_expQuadraticYdrift_useExpectationOnYdrift(DelarueMenozzi_expQuadraticYdrift):
    '''
    dX_t = -Y_t dt + \sigma dW_t
    dY_t = eta_t dt + Z_t dW_t
    X_0 = x_0, Y_T = X_T
    
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

'''
def iterate_expQuadraticYdrift(iter_number = 20, *args, **kwargs):
    eta = None
    system = None
    all_etas = [] 
    for i in range(iter_number):
        print("start {i}th iteration".format(i=i))
        if i == 0:
            system = DelarueMenozzi_expQuadraticYdrift(*args, **kwargs)
        else:
            system = DelarueMenozzi_expQuadraticYdrift_useExpectationOnYdrift(eta = eta,
                                                                              *args,
                                                                              **kwargs)
        system.compute_all_link()
        system.simulate_forward()
        eta = system.expectation_g_Y
        all_etas.append(eta)
    return all_etas
'''        