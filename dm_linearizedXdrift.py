'''
Created on Jan 28, 2016

@author: weiluo
'''

from dm_expXdrift import DM_expXdrift


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