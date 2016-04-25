'''
Created on Jan 29, 2016

@author: weiluo
'''

import sys
from run_dm_iteration_helpers import *
from dm_expXdrift import dm_iterate_then_pickle_expXdrift_linearYdrift, dm_use_eta_then_pickle_expXdrift_linearYdrift
from run_dm_linearizedXdrift_linearYdrift import generate_tradingModel_parser

def run_dm_expXdrift_linearYdrift_use_eta():
    parser = generate_tradingModel_parser() 
    parser.add_argument('-eta_path',  help='the path of all etas')

    arg_dict, file_name = prepare_argdict_and_filename_from_parser(
                            parser, 
                            {"model_type": "expXdrift_linearYdrift"},
                            lambda k, v: v and (k != 'prefix'))
    dm_use_eta_then_pickle_expXdrift_linearYdrift(file_name, 
                                                  **arg_dict)
    
    
  


if __name__ == '__main__':
    sys.exit(run_dm_expXdrift_linearYdrift_use_eta())