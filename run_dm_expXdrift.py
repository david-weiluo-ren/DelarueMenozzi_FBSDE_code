'''
Created on Jan 28, 2016

@author: weiluo
'''
import argparse, sys
from dm_expXdrift import iterate_expXdrift

def run_dm_expXdrift():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--x_0', type=float, nargs='?', help='x0')
    parser.add_argument('--M_time', type=float, nargs='?', help='M_Time')
    parser.add_argument('--M_space', type=float,  nargs='?', help='M_Space')
    parser.add_argument('--sigma', type=float,  nargs='?', help='sigma')
    parser.add_argument('--iter_number', type=int,nargs='?', help='number of iteration')
    parser.add_argument('--num_MC_path', type=int, help='numbder of sampling paths in MC')
    parser.add_argument('--prefix', type=str, help='prefix of the name of figure')
    parser.add_argument('--delta_time', type=float,nargs='?', help='time step size')
    parser.add_argument('--delta_space', type=float,nargs='?', help='spatial step size')
    parser.add_argument('--exp_y0', type=float,nargs='?', help='empirical initialization')
    parser.add_argument('--A', type=float,nargs='?', help='A in drift of X')
    parser.add_argument('--kappa', type=float,nargs='?', help='A in drift of X')
    parser.add_argument('--m', type=float,nargs='?', help='terminal condition')
    parser.add_argument('--beta', type=float,nargs='?', help='beta in drift Y')

    args = {k: v for k, v in vars(parser.parse_args()).items() if v}
    for k, v in args.items():
        print(k, v)

   
    iterate_expXdrift(**args)
    


if __name__ == '__main__':
    sys.exit(run_dm_expXdrift())
    