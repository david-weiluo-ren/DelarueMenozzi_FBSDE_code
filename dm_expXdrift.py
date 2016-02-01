'''
Created on Jan 28, 2016

@author: weiluo
'''

from importlib import reload
import delarueMenozzi_simplifedCase_base
reload(delarueMenozzi_simplifedCase_base)

from delarueMenozzi_simplifedCase_base import DelarueMenozziSimplifiedCaseBase

import numpy as np

class DM_expXdrift(DelarueMenozziSimplifiedCaseBase):
    '''
    dQ_t = [Ae^{-\kappa \Delta^b_t} - Ae^{-\kappa \Delta^a_t}] dt + \sigma dB_t
    dY_t = -2\beta * EY_0 * e^{-2\beta t} dt + Z_t dB_t
    Q_0 = q_0; Y_T = -2m Q_T
    where \Delta^b_t = 1 / \kappa - Y_t; \Delta^a_t = 1 / \kappa + Y_t
    
    ==>
    
    dX_t = Ae^{-1}[e^{\kappa Y_t} - e^{-\kappa Y_t}] dt + \sigma dW_t
    dY_t = -2 \beta * x * e^{-2\beta t} dt + Z_t dW_t
    X_0 = x_0, Y_T = -2m * X_T
    
    We want to compute the distribution of
    Y_0
    '''


    def __init__(self, 
                 expected_y0 = 1, 
                 A = 1, 
                 kappa = 1, 
                 m = 0.05, 
                 beta = 1,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.A = A
        self.kappa = kappa
        self.m = m
        self.expected_y0 = expected_y0
        self.beta = beta
    def F(self, x, y):
        exp_y = np.exp(-self.kappa * y)
        return self.A * np.exp(-1) * (exp_y - 1 / exp_y)
    def G(self, time_index, y):
        return -2 * self.beta * self.expected_y0 * np.exp(-2 * self.beta * self.time_grid[time_index])
    
    def g(self, y):
        return y
    def f(self, x):
        return -2 * self.m * x
    def compute_expY_0(self):
        return self.link[-1][self.spatial_point_to_index(self.x_0)]
    
    
class DM_expXdrift_linearYdrift(DM_expXdrift):
    '''
    dQ_t = [Ae^{-\kappa \Delta^b_t} - Ae^{-\kappa \Delta^a_t}] dt + \sigma dB_t
    dY_t = -2\beta Y_t dt + Z_t dB_t
    Q_0 = q_0; Y_T = -2m Q_T
    where \Delta^b_t = 1 / \kappa - Y_t; \Delta^a_t = 1 / \kappa + Y_t
    
    ==>
    
    dX_t = Ae^{-1}[e^{\kappa Y_t} - e^{-\kappa Y_t}] dt + \sigma dW_t
    dY_t = -2 \beta * Y_t dt + Z_t dW_t
    X_0 = x_0, Y_T = -2m * X_T
    
    We want to compute the distribution of
    Y_0
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def G(self, time_index, y):
        return -2 * self.beta * y
    
    
 
    