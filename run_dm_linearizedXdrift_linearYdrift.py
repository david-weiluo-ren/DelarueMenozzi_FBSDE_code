'''
Created on Jan 29, 2016

@author: weiluo
'''

import sys
from run_dm_iteration_helpers import *
from dm_linearizedXdrift import dm_iterate_then_pickle_linearizedXdrift_linearYdrift

def add_tradingModel_argument_to_parser(parser):
    parser.add_argument('-A', type=float,nargs='?', help='A in drift of X')
    parser.add_argument('-kappa', type=float,nargs='?', help='kappa in drift of X')
    parser.add_argument('-beta', type=float, nargs='?', help='beta in drift of Y')
    parser.add_argument('-m', type=float,nargs='?', help='terminal condition')
    return parser

def generate_tradingModel_parser():
    parser = argparse.ArgumentParser()
    parser = add_dm_sharing_argument_to_parser(parser)
    parser = add_tradingModel_argument_to_parser(parser)
    return parser

def run_dm_linearizedXdrift_linearYdrift():
    parser = generate_tradingModel_parser()
    arg_dict, file_name = prepare_argdict_and_filename_from_parser(
                            parser, 
                            {"model_type": "linearXdrift_linearYdrift"},
                            lambda k, v: v and (k != 'prefix'))
    dm_iterate_then_pickle_linearizedXdrift_linearYdrift(file_name, **arg_dict)
    
    
  


if __name__ == '__main__':
    sys.exit(run_dm_linearizedXdrift_linearYdrift())