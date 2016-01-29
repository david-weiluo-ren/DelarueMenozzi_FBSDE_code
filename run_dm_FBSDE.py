'''
Created on Jan 28, 2016

@author: weiluo
'''
import argparse, sys
from dm_expXdrift import DM_expXdrift
from dm_linearizedXdrift import DM_linearizedXdrift
from run_dm_iteration_helpers import add_dm_sharing_argument_to_parser
def model_factory(model_type, *args, **kwargs):
    if model_type =="exp":
        return DM_expXdrift(*args, **kwargs)
    elif model_type == "linear":
        return DM_linearizedXdrift(*args, **kwargs)
    else:
        raise Exception("model type should be "
                        + "either 'exp' for exponential model"
                        + "or 'linear' for linearized model")
    
    
def iterate_helper(model_type, iter_number = 20, expected_y0 = 0.5, *args, **kwargs):
    system = None
    all_expected_y0 = [expected_y0]
    for i in range(iter_number):
        print("start {i}th iteration".format(i = i))
        system = model_factory(model_type, expected_y0 = all_expected_y0[-1], *args, **kwargs)
        system.compute_all_link()
        all_expected_y0.append(system.compute_expY_0())
        print("expectation of y0 = {expected_y0}".format(expected_y0 = all_expected_y0[-1]))
        
    return all_expected_y0   

def iterate_expXdrift(iter_number = 20, expected_y0 = 0.5, *args, **kwargs):
    return iterate_helper('exp', iter_number, expected_y0, *args, **kwargs)

def iterate_linearizedXdrift(iter_number = 20, expected_y0 = 0.5, *args, **kwargs):
    return iterate_helper('linear', iter_number, expected_y0, *args, **kwargs)


def run_dm_FBSDE():
    parser = argparse.ArgumentParser()
    parser = add_dm_sharing_argument_to_parser(parser)
    parser.add_argument('model_type', type = str, help="exp: expXdrift model; linear: linearizedXdrift model")
    parser.add_argument('-expected_y0', type=float,nargs='?', help='initial expected y0')
    parser.add_argument('-A', type=float,nargs='?', help='A in drift of X')
    parser.add_argument('-kappa', type=float,nargs='?', help='A in drift of X')
    parser.add_argument('-m', type=float,nargs='?', help='terminal condition')
    parser.add_argument('-beta', type=float,nargs='?', help='beta in drift Y')
    args = {k: v for k, v in vars(parser.parse_args()).items() if v}
    for k, v in args.items():
        print(k, v)
    prefix = args.pop('prefix') if 'prefix' in args else ''
    args_str = ("{}{}".format(k, v) for k, v in args.items())
    filename = prefix + ("_".join(args_str))
    model_type = args.pop('model_type')

    all_expected_y0 = iterate_helper(model_type, **args)
    
    
    with open(filename, 'w') as filehandler:
        for expected_y0 in all_expected_y0:
            filehandler.write("{}\n".format(expected_y0))
    
    


if __name__ == '__main__':
    sys.exit(run_dm_FBSDE())
    