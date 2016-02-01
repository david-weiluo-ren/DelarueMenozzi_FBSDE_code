'''
Created on Jan 28, 2016

@author: weiluo
'''
import argparse, sys
from dm_expXdrift import DM_expXdrift, DM_expXdrift_linearYdrift
from dm_linearizedXdrift import DM_linearizedXdrift,\
    DM_linearizedXdrift_linearYdrift
from run_dm_iteration_helpers import add_dm_sharing_argument_to_parser, \
    prepare_argdict_and_filename_from_parser
def model_factory(model_type, expected_y0 = None, *args, **kwargs):
    
    
    if expected_y0:
        if model_type =="exp":
            return DM_expXdrift(expected_y0=expected_y0, *args, **kwargs)
        elif model_type == "linear":
            return DM_linearizedXdrift(expected_y0=expected_y0, *args, **kwargs)
        else:
            raise Exception("model type should be "
                        + "either 'exp' for exponential model"
                        + "or 'linear' for linearized model")
    else:
        if model_type =="exp":
            return DM_expXdrift_linearYdrift(*args, **kwargs)
        elif model_type == "linear":
            return DM_linearizedXdrift_linearYdrift(*args, **kwargs)
        else:
            raise Exception("model type should be "
                        + "either 'exp' for exponential model"
                        + "or 'linear' for linearized model")
    
    
def iterate_helper_withIinitialExpectedY0(model_type, iter_number = 20, expected_y0 = 0.5, *args, **kwargs):
    system = None
    all_expected_y0 = [expected_y0]
    for i in range(iter_number):
        print("start {i}th iteration".format(i = i))
        system = model_factory(model_type, expected_y0 = all_expected_y0[-1], *args, **kwargs)
        system.compute_all_link()
        all_expected_y0.append(system.compute_expY_0())
        print("expectation of y0 = {expected_y0}".format(expected_y0 = all_expected_y0[-1]))
        
    return all_expected_y0   

def iterate_helper_withoutIinitialExpectedY0(model_type, iter_number = 20, *args, **kwargs):
    print("no initial expected y0, your specified y0 would be discarded.")
    if 'expected_y0' in kwargs:
        del kwargs['expected_y0']
    
    
    system = None
    all_expected_y0 = []
    for i in range(iter_number):
        print("start {i}th iteration".format(i = i))
            
        system = model_factory(model_type, expected_y0 = all_expected_y0[-1], *args, **kwargs) \
                 if i > 0 \
                 else model_factory(model_type, expected_y0 = None, *args, **kwargs)
        system.compute_all_link()
        all_expected_y0.append(system.compute_expY_0())
        print("expectation of y0 = {expected_y0}".format(expected_y0 = all_expected_y0[-1]))
        
    return all_expected_y0  

def iterate_expXdrift(iter_number = 20, expected_y0 = None, *args, **kwargs):
    if expected_y0:
        return iterate_helper_withIinitialExpectedY0('exp', iter_number, expected_y0, *args, **kwargs)
    else:
        return iterate_helper_withoutIinitialExpectedY0('exp', iter_number, *args, **kwargs)


def iterate_linearizedXdrift(iter_number = 20, expected_y0 = None, *args, **kwargs):
    if expected_y0:
        return iterate_helper_withIinitialExpectedY0('linear', iter_number, expected_y0, *args, **kwargs)
    else:
        return iterate_helper_withoutIinitialExpectedY0('linear', iter_number, *args, **kwargs)



def generate_dm_FBSDE_parser(parser):
    parser = add_dm_sharing_argument_to_parser(parser)
    parser.add_argument('model_type', type = str, help="exp: expXdrift model; linear: linearizedXdrift model")
    parser.add_argument('-expected_y0', type=float,nargs='?', help='initial expected y0')
    parser.add_argument('-A', type=float,nargs='?', help='A in drift of X')
    parser.add_argument('-kappa', type=float,nargs='?', help='kappa in drift of X')
    parser.add_argument('-m', type=float,nargs='?', help='terminal condition')
    parser.add_argument('-beta', type=float,nargs='?', help='beta in drift Y')
    parser.add_argument('--initExpectedY0', dest='initial_expectedY0', action='store_true')
    parser.add_argument('--no-initExpectedY0', dest='initial_expectedY0', action='store_false')
    parser.set_defaults(initial_expectedY0=False)
    return parser

    

class DM_FBSDE_runner():
    def __init__(self, 
                 generate_dm_FBSDE_parser_func):
        self.parser = argparse.ArgumentParser()
        self.parser = generate_dm_FBSDE_parser_func(self.parser)

        self.model_type = None
        self.use_initial_expectedY0 = None
        
        self.arg_dict = None
        self.file_name = None
    def generate_argument(self):
        self.model_type = self.parser.parse_args().model_type
        self.use_initial_expectedY0 = self.parser.parse_args().initial_expectedY0
        self.arg_dict, self.file_name = prepare_argdict_and_filename_from_parser(
                            self.parser, 
                            {'model_type' : self.model_type},
                            lambda k, v: v and (k != 'prefix') 
                                           and (k != 'model_type')
                                           and (k != 'initial_expectedY0'))



def run_dm_FBSDE():
    dm_FBSDE_runner = DM_FBSDE_runner(generate_dm_FBSDE_parser)
    dm_FBSDE_runner.generate_argument()
    
    print("model_type ", dm_FBSDE_runner.model_type)
    
    all_expected_y0 = iterate_helper_withIinitialExpectedY0(dm_FBSDE_runner.model_type, 
                                                            **dm_FBSDE_runner.arg_dict)\
                      if dm_FBSDE_runner.use_initial_expectedY0\
                      else iterate_helper_withoutIinitialExpectedY0(dm_FBSDE_runner.model_type, 
                                                                    **dm_FBSDE_runner.arg_dict)
    
    
    with open(dm_FBSDE_runner.file_name, 'w') as file_handler:
        for expected_y0 in all_expected_y0:
            file_handler.write("{}\n".format(expected_y0))
    
    




if __name__ == '__main__':
    sys.exit(run_dm_FBSDE())
    