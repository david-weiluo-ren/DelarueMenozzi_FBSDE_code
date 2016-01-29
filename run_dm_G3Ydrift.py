'''
Created on Jan 29, 2016

@author: weiluo
'''

import sys
from run_dm_iteration_helpers import *
from delarueMenozzi_G3Ydrift import dm_iterate_then_pickle_G3Ydrift


def run_dm_G3Ydrift():
    parser = argparse.ArgumentParser()
    parser = add_dm_sharing_argument_to_parser(parser)
    parser.add_argument('-a', type=float,nargs='?', help='a in drift of Y, constant before G3')
    parser.add_argument('-m', type=float,nargs='?', help='terminal condition')

    
    arg_dict, file_name = prepare_argdict_and_filename_from_parser(
                            parser, 
                            lambda k, v: v and (k != 'prefix'))
    dm_iterate_then_pickle_G3Ydrift(file_name, **arg_dict)
    
    
  


if __name__ == '__main__':
    sys.exit(run_dm_G3Ydrift())