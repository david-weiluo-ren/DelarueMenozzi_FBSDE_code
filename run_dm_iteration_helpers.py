'''
Created on Jan 28, 2016

@author: weiluo
'''
import argparse, pickle
import numpy as np


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

def generate_file_name_from_dict(prefix, info, arg_dict):
    info_str = '_'.join('{}_{}'.format(k, v) for k, v in info.items())
    
    args_str = ("{}{}".format(k, v) for k, v in sorted(arg_dict.items()))
    return prefix + info_str + '_' + ("_".join(args_str))

def dm_iterate_then_pickle(model_factory, file_name, *args, **kwargs):
    all_etas = dm_iterate_helper(model_factory, *args, **kwargs)
    with open(file_name, 'wb') as file_handler:
        pickle.dump(all_etas, file_handler)

    
    
def prepare_argdict_and_filename_from_parser(parser, info, k_v_predicate):
    args = parser.parse_args()
    arg_dict = {k: v for k, v in vars(args).items() 
                if k_v_predicate(k, v)}
    
    for k, v in arg_dict.items():
        print(k, v)
        
    file_name = generate_file_name_from_dict(prefix = args.prefix or '',
                                             info = info,
                                            arg_dict = arg_dict)    
    
    return (arg_dict, file_name)


    
    