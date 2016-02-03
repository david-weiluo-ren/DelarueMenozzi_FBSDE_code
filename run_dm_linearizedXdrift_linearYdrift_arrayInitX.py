'''
Created on Jan 29, 2016

@author: weiluo
'''

import sys, pickle
from run_dm_iteration_helpers import *
from run_dm_FBSDE_arrayOfInitialX import add_initX_arg_parser

from dm_linearizedXdrift import iterate_linearXdrift_linearYdrift
from dm_expXdrift import iterate_expXdrift_linearYdrift
def generate_parser_FBSDE_linearYdrift(parser):
    parser.add_argument('-A', type=float,nargs='?', help='A in drift of X')
    parser.add_argument('-kappa', type=float,nargs='?', help='kappa in drift of X')
    parser.add_argument('-m', type=float,nargs='?', help='terminal condition')
    return parser

def run_dm_linearized_or_exp_Xdrift_linearYdrift_arrayInitX_helper(xdrift_type):
    '''
    xdrift_type should be either 'linear' or 'exp'
    '''
    
    assert(xdrift_type == 'linear' or xdrift_type == 'exp')
    parser = argparse.ArgumentParser()
    parser = add_dm_sharing_argument_to_parser(parser)
    parser = generate_parser_FBSDE_linearYdrift(parser)
    parser = add_initX_arg_parser(parser)
    arg_dict, file_name = prepare_argdict_and_filename_from_parser(
                            parser, 
                            {"model_type": xdrift_type+"Xdrift_linearYdrift"},
                            lambda k, v: v and (k != 'prefix'))
    
    init_x_array = np.arange(0,
                 abs(arg_dict['initX_bound']),
                 arg_dict['initX_deltaX'])
    del arg_dict['initX_bound']
    del arg_dict['initX_deltaX']
    if 'x_0' in arg_dict:
        del arg_dict['x_0']
    
    initX_eta_list = []
    for init_x in init_x_array:
        print("init_x: {}".format(init_x))
        eta = iterate_linearXdrift_linearYdrift(x_0 = init_x, **arg_dict)\
              if xdrift_type == 'linear'\
              else iterate_expXdrift_linearYdrift(x_0 = init_x, **arg_dict)
        initX_eta_list.append((init_x, eta))
    
    with open(file_name, 'wb') as file_handler:
        pickle.dump(initX_eta_list, file_handler)
    
    
    
    
  


if __name__ == '__main__':
    sys.exit(run_dm_linearized_or_exp_Xdrift_linearYdrift_arrayInitX_helper('linear'))