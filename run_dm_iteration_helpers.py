'''
Created on Jan 28, 2016

@author: weiluo
'''
import argparse





def dm_iterate_helper(model_factory, iter_number = 20, *args, **kwargs):
    eta = None
    system = None
    all_etas = [] 
    for i in range(iter_number):
        print("start {i}th iteration".format(i=i))
        if i == 0:
            system = model_factory('init', *args, **kwargs)
        else:
            system = model_factory('use_expectation',
                                   eta = eta, 
                                   *args, 
                                   **kwargs)
        system.compute_all_link()
        system.simulate_forward()
        eta = system.expectation_g_Y
        all_etas.append(eta)
    return all_etas

def add_dm_sharing_argument_to_parser(parser):
    parser.add_argument('-x_0', type=float, nargs='?', help='x0')
    parser.add_argument('-M_time', type=float, nargs='?', help='M_Time')
    parser.add_argument('-M_space', type=float,  nargs='?', help='M_Space')
    parser.add_argument('-sigma', type=float,  nargs='?', help='sigma')
    parser.add_argument('-iter_number', type=int,nargs='?', help='number of iteration')
    parser.add_argument('-num_MC_path', type=int, help='numbder of sampling paths in MC')
    parser.add_argument('-prefix', type=str, help='prefix of the name of figure')
    parser.add_argument('-delta_time', type=float,nargs='?', help='time step size')
    parser.add_argument('-delta_space', type=float,nargs='?', help='spatial step size')
    return parser
    
    