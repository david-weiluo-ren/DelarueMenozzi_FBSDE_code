'''
Created on Jan 27, 2016

@author: weiluo
'''
from importlib import reload
import delarueMenozzi_simplifedCase_base
reload(delarueMenozzi_simplifedCase_base)

from delarueMenozzi_simplifedCase_base import DelarueMenozziSimplifiedCaseBase
import numpy as np

class DelarueMenozzi_expQuadraticYdrift(DelarueMenozziSimplifiedCaseBase):
    '''
    dX_t = -Y_t dt + \sigma dW_t
    dY_t = A * e^{- \kappa^2 Y_t} dt + Z_t dW_t
    X_0 = x_0, Y_T = X_T
    
    We want to compute the distribution of
    g(Y_t) from 0 to T.
    g = A * e^{- \kappa^2 Y_t}
    '''

    def __init__(self, A = 1, kappa = 1, *args, **kwargs):
        self.A = A
        self.kappa = kappa
        super().__init__(*args, **kwargs)
    
    def F(self, x, y):
        return -1 * y
    def G(self, time_index, y):
        return self.g_G_helper(time_index, y)
    def f(self, x):
        return x
    def g(self, y):
        return self.g_G_helper(0, y)
    
    def g_G_helper(self, time_index, y):
        return self.A * np.exp(-1 * self.kappa * (y ** 2))