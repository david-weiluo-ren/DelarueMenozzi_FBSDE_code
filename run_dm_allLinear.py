'''
Created on Jan 29, 2016

@author: weiluo
'''

import sys
from run_dm_iteration_helpers import *
from delarueMenozzi_allLinear import dm_iterate_then_pickle_allLinear

def run_dm_allLinear():
    parser = argparse.ArgumentParser()
    parser = add_dm_sharing_argument_to_parser(parser)
    parser.add_argument('-K', type=float,nargs='?', help='K in drift of Y')
    parser.add_argument('-m', type=float,nargs='?', help='terminal condition')

    
    arg_dict, file_name = prepare_argdict_and_filename_from_parser(
                            parser, 
                            {"model_type": "allLinear"},
                            lambda k, v: v and (k != 'prefix'))
    dm_iterate_then_pickle_allLinear(file_name, **arg_dict)
    
    
  


if __name__ == '__main__':
    sys.exit(run_dm_allLinear())