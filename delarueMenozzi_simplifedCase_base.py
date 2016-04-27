'''
Created on Jan 27, 2016

@author: weiluo




'''
import numpy as np



class DelarueMenozziSimplifiedCaseBase:
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
        self.link[:] = []
        self.link.append(self.f(self.space_grid))
        
    def one_step_back(self, time_index):
        curr_link = self.link[-1]
        new_link = [self.monte_carlo_one_point(curr_link, 
                                               x_index, 
                                               time_index) 
                    for x_index in range(self.num_space_grid)]
        self.link.append(np.array(new_link))
    
    
    def monte_carlo_one_point(self,
                              curr_link,
                              x_index,
                              time_index):
        MC_sample = np.random.randn(self.num_MC_path) * np.sqrt(self.delta_time)
        x_value = self.space_grid[x_index]
        approximated_y_value = curr_link[x_index]
        simulation_result = self.function_to_simulate(time_index,
                                                      x_value,
                                                      approximated_y_value,
                                                      curr_link,
                                                      MC_sample)
        return np.mean(simulation_result) - self.compute_Y_drift(time_index,
                                                                 approximated_y_value)
     
    def function_to_simulate(self,
                             time_index,
                             x_value,
                             y_value,
                             curr_link,
                             MC_sample):
        simulated_new_x = x_value + self.F(time_index, x_value, y_value) * self.delta_time + self.sigma*MC_sample

        return curr_link[self.spatial_point_to_index(simulated_new_x)]
                
    def spatial_point_to_index(self, x):
        return (np.true_divide(self.project_inside_spatial_grid(x)+self.M_space, 
                               self.delta_space) 
                + 0.5).astype(int)

    def project_inside_spatial_grid(self, x):
        return np.minimum(np.maximum(x, -1*self.M_space), self.M_space - self.delta_space)
   
        
    def compute_Y_drift(self, time_index, y_value):
        return self.G(time_index, y_value) * self.delta_time
        
        
        
    def compute_all_link(self):
        self.initialization()

        for i in range(self.num_time_grid):
            self.one_step_back(-1 * (i + 1))
        
    def simulate_forward(self, func=None):
        self.forward_variable[:] = [self.x_0 * np.ones(self.num_MC_path)]
        self.expectation_g_Y[:] = []

        if not func:
            func = self.one_step_forward
        y_0 = self.link[-1][self.spatial_point_to_index(self.x_0)]
        self.expectation_g_Y.append(self.g(y_0))
        for i in range(self.num_time_grid):
            func(i)
    
    def one_step_forward(self, time_index):
        curr_link = self.link[-1 * (time_index + 1)]
        next_link = self.link[-1 * (time_index + 2)]
        MC_sample = np.random.randn(self.num_MC_path) * np.sqrt(self.delta_time)
        curr_forward = self.forward_variable[-1]
        curr_backward = curr_link[self.spatial_point_to_index(curr_forward)]
        forward_increment = self.F(time_index,
                                   curr_forward, 
                                   curr_backward) * self.delta_time + self.sigma * MC_sample
        new_forward = curr_forward + forward_increment
        new_backward = next_link[self.spatial_point_to_index(new_forward)]
        self.forward_variable.append(new_forward)
        self.expectation_g_Y.append(np.mean(self.g(new_backward)))                                   
        
        
    
    
            
        
        
        
        
        
        