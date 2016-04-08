'''
Created on Jan 27, 2016

@author: weiluo




'''
import numpy as np

from delarueMenozzi_expQuadraticYdrift import DelarueMenozzi_expQuadraticYdrift
from types import MethodType, FunctionType
class DelarueMenozziSimplifiedCaseBase_refactored:
    '''
    dX_t = F(X_t, Y_t) dt + \sigma dW_t
    dY_t = G(t, Y_t) dt + Z_t dW_t
    X_0 = x_0, Y_T = f(X_T)
    
    We want to compute the distribution of
    g(Y_t) from 0 to T.
    '''
    

    def __init__(self, 
                 sigma = 0.05,
                 x_0 = 1,
                 delta_time = 0.1,
                 M_time = 1,
                 delta_space = 0.01,
                 M_space = 10,
                 num_MC_path = 10000):
        self.sigma = sigma
        self.x_0 = x_0
        
        
        '''
        time space discretization.
        '''
        self.delta_time = delta_time
        self.M_time = M_time
        self.time_grid = np.arange(0, self.M_time, self.delta_time)
        self.num_time_grid = len(self.time_grid)
        
        
        '''
        spatial space discretization
        '''
        self.delta_space = delta_space
        self.M_space = M_space
        self.space_grid = np.arange(-1 * self.M_space, 
                                    self.M_space, 
                                    self.delta_space)
        self.num_space_grid = len(self.space_grid)
        
        
        
        
        self.num_MC_path = num_MC_path
        self.forward_variable = [self.x_0 * np.ones(self.num_MC_path)]
        self.link = []
        self.expectation_g_Y = []
        
        

    
        
    def initialization(self):
        self.link.append(self.f(self.space_grid))
        
    def one_step_back(self, time_index):
        curr_link = self.link[-1]
        new_link = self.monte_carlo(curr_link, time_index) 
                    
        self.link.append(np.asarray(new_link))
    
    
    def monte_carlo(self, curr_link, time_index):
        MC_sample = np.random.randn(self.num_MC_path, self.num_space_grid) * np.sqrt(self.delta_time)
        all_x_value = self.space_grid
        all_approximated_y_value = curr_link
        '''
        simulation_result = self.function_to_simulate(all_x_value,
                                                      all_approximated_y_value,
                                                      curr_link,
                                                      MC_sample)
        del MC_sample
        return np.mean(simulation_result, axis=0) - self.compute_Y_drift(time_index,
                                                                 all_approximated_y_value)
        '''
        return self.average_function_to_simulate(time_index, 
                                                 all_x_value, 
                                                 all_approximated_y_value,
                                                 curr_link, 
                                                 MC_sample) - self.compute_Y_drift(time_index,
                                                                 all_approximated_y_value)
    def function_to_simulate(self,
                             time_index,
                             all_x_value,
                             all_y_value,
                             curr_link,
                             MC_sample):
        simulated_new_x = all_x_value + self.F(time_index, all_x_value, all_y_value) * self.delta_time + self.sigma * MC_sample
        tmp1 = self.spatial_point_to_index(simulated_new_x).tolist()
        tmp = [curr_link[sim] for sim in tmp1]
        return np.array(tmp)
    
    
    def average_function_to_simulate2(self,
                                      time_index, 
                             all_x_value,
                             all_y_value,
                             curr_link,
                             MC_sample):
        
        simulated_new_x = all_x_value + self.F(time_index, all_x_value, all_y_value) * self.delta_time + self.sigma * MC_sample
        tmp1 = self.spatial_point_to_index(simulated_new_x).T
        return np.array([np.mean(curr_link[oneDatumSimulation.tolist()]) for oneDatumSimulation in tmp1])
        
    def average_function_to_simulate(self,
                             time_index, 
                             all_x_value,
                             all_y_value,
                             curr_link,
                             MC_sample):
        MC_sample_T = MC_sample.T
        return np.array([np.mean(curr_link[self.spatial_point_to_index(all_x_value[i]
                                                                       + self.F(time_index, all_x_value[i], all_y_value[i]) * self.delta_time 
                                                                       + self.sigma * MC_sample_T[i])]) 
                         for i in range(self.num_space_grid)])
              
    def spatial_point_to_index(self, x):
        return (np.true_divide(self.project_inside_spatial_grid(x)+self.M_space, 
                               self.delta_space) 
                + 0.5).astype(int)

    def project_inside_spatial_grid(self, x):
        return np.minimum(np.maximum(x, -1*self.M_space), self.M_space - self.delta_space)
   
        
    def compute_Y_drift(self, time_index, all_y_value):
        return self.G(time_index, all_y_value) * self.delta_time
        
        
        
    def compute_all_link(self):
        self.initialization()

        for i in range(self.num_time_grid):
            self.one_step_back(-1 * (i + 1))
        
    def simulate_forward(self):
        y_0 = self.link[-1][self.spatial_point_to_index(self.x_0)]
        self.expectation_g_Y.append(y_0)
        for i in range(self.num_time_grid):
            self.one_step_forward(i)
    
    def one_step_forward(self, time_index):
        curr_link = self.link[-1 * (time_index + 1)]
        next_link = self.link[-1 * (time_index + 2)]
        MC_sample = np.random.randn(self.num_MC_path) * np.sqrt(self.delta_time)
        curr_forward = self.forward_variable[-1]
        curr_backward = curr_link[self.spatial_point_to_index(curr_forward)]
        forward_increment = self.F(time_index, 
                                   curr_forward, 
                                   curr_backward) * self.delta_time * self.sigma + MC_sample
        new_forward = curr_backward + forward_increment
        new_backward = next_link[self.spatial_point_to_index(new_forward)]
        self.forward_variable.append(new_forward)
        self.expectation_g_Y.append(np.mean(self.g(new_backward)))                                   
        
class DelarueMenozzi_expQuadraticYdrift_refactored(DelarueMenozziSimplifiedCaseBase_refactored):
    
    def __init__(self, normal_obj, A = 1, kappa = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.A = A
        self.kappa = kappa
    
        for attr_name, attr in normal_obj.__class__.__dict__.items():
            if (not attr_name.startswith("__")) and (attr_name not in self.__class__.__dict__) and isinstance(attr, FunctionType):
                setattr(self, attr_name, MethodType(attr, self))
    
        
        
        
        
        
        