'''
Created on Jan 31, 2016

@author: weiluo
'''

from run_dm_FBSDE import DM_FBSDE_runner, generate_dm_FBSDE_parser,\
    iterate_helper_withIinitialExpectedY0,\
    iterate_helper_withoutIinitialExpectedY0
import numpy as np
import sys
def generate_dm_FBSDE_arrayOfInitialX_parser(parser):
    parser = generate_dm_FBSDE_parser(parser)
    parser.add_argument('-initX_bound', type=float,nargs='?', default=5, help='bound of initial X used in simulation')
    parser.add_argument('-initX_deltaX', type=float,nargs='?', default=0.05, help='step size of initial X used in simulation')
    return parser

    


def run_dm_FBSDE_arrayOfInitialX():
    dm_FBSDE_runner = DM_FBSDE_runner(generate_dm_FBSDE_arrayOfInitialX_parser)
    dm_FBSDE_runner.generate_argument()
    
    init_x_array = np.arange(-1 * abs(dm_FBSDE_runner.arg_dict['initX_bound']),
                 abs(dm_FBSDE_runner.arg_dict['initX_bound']),
                 dm_FBSDE_runner.arg_dict['initX_deltaX'])
    del dm_FBSDE_runner.arg_dict['initX_bound']
    del dm_FBSDE_runner.arg_dict['initX_deltaX']
    if 'x_0' in dm_FBSDE_runner.arg_dict:
        del dm_FBSDE_runner.arg_dict['x_0']
    initX_y0_list = []
    for init_x in init_x_array:
        all_expected_y0 = iterate_helper_withIinitialExpectedY0(dm_FBSDE_runner.model_type, 
                                                                x_0 = init_x,
                                                            **dm_FBSDE_runner.arg_dict)\
                      if dm_FBSDE_runner.use_initial_expectedY0\
                      else iterate_helper_withoutIinitialExpectedY0(dm_FBSDE_runner.model_type, 
                                                                    x_0 = init_x,
                                                                    **dm_FBSDE_runner.arg_dict)
        
        initX_y0_list.append((init_x, all_expected_y0[-1]))
    
    with open(dm_FBSDE_runner.file_name, 'w') as file_handler:
        for init_x, y_0 in all_expected_y0:
            file_handler.write("init_x: {}, y0: {}".format(init_x, y_0))
    
if __name__ == '__main__':
    sys.exit(run_dm_FBSDE_arrayOfInitialX())