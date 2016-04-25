import pickle
import numpy as np
import matplotlib
#matplotlib.use('PS')
from matplotlib import pyplot as plt
import seaborn

seaborn.set(rc={"lines.linewidth": 2})


def trading_exp_theo(y_0,
                     beta=1.0,
                     t_space=np.arange(0,1,0.01)):
    return y_0 * np.exp(2 * beta *  - t_space)


def trading_linear_theo(x_0=1,
                        m=0.1,
                        A=30.0,
                        kappa=0.001,
                        beta=1.0,
                        t_space=np.arange(0,1,0.01)):
    coef = -np.true_divide(x_0,
                           0.5/m + A/np.exp(1) * kappa/beta * (np.exp(2 * beta * np.max(t_space)) - 1))
    return coef * np.exp(2 * beta * (np.max(t_space) - t_space))

def iteration_figure_helper(iteration_data,
                            iterations_to_show,
                            select_func,
                            figure_ax=None,
                            figure_name=None,
                            x_array_limit=None,
                            xlabel="",
                            ylabel="", 
                            other=None):
    num_iterations = len(iteration_data)
    x_array = np.linspace(0, x_array_limit, len(iteration_data[0])) if x_array_limit else np.arange(0, len(iteration_data[0]))
    for i in iterations_to_show:
        if i < 0:
            i = num_iterations + i
        if figure_ax:
            figure_ax.plot(x_array, select_func(iteration_data, i), label="iterations {}".format(i + 1))
        else:
            plt.plot(x_array, select_func(iteration_data, i), label="iterations {}".format(i + 1))
    other
        
    if figure_ax:
        figure_ax.set_xlabel(xlabel)
        figure_ax.set_ylabel(ylabel)
        figure_ax.legend(loc="best")
    else:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(loc="best")
    if figure_name:
        plt.savefig(figure_name) 


def iteration_figure(iteration_data,
                     iterations_to_show,
                     *args, **kwargs):
    return iteration_figure_helper(iteration_data,
                                   iterations_to_show,
                                   lambda data, i: data[i],
                                   *args, **kwargs)
    
def iteration_difference_figure(iteration_data,
                                iterations_to_show,
                                *args, **kwargs):
    return iteration_figure_helper(iteration_data,
                                   iterations_to_show,
                                   lambda data, i: data[i] - data[-1],
                                   *args, **kwargs)


def trading_iteration_figure():
    file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" + 
                    "model_type_expXdrift_linearYdrift_A0.05_M_space10.0_M_time3.0_beta0.2_delta_space0.005_delta_time0.01_iter_number8_kappa1.6_m0.2_num_MC_path100000_sigma3.0_x_03.0",
                    'rb')
    tmp = pickle.load(file_handler)
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 10))
    plt.suptitle("convergence of outputs from each iteration",
            y=0.95, size=18)
    iteration_figure(tmp, 
                 [0,1,2,3,-2,-1],
                 figure_ax=ax1,
                 x_array_limit=3,
                 xlabel="time",
                 ylabel="function value")
    iteration_difference_figure(tmp, 
                            [0,1,2,3,-2],
                            figure_ax=ax2,
                            x_array_limit=3,
                            xlabel="time",
                            ylabel="difference from final output")
    plt.savefig("trading_iteration_figure.png")
    
    
def trading_iteration_figure2():
    #file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" + 
    #                "model_type_expXdrift_linearYdrift_A0.1_M_space10.0_M_time3.0_beta0.1_delta_space0.005_delta_time0.01_iter_number6_kappa3.0_m0.1_num_MC_path100000_sigma2.0_x_02.0",
    #                'rb')
    file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" +                  
                     "model_type_expXdrift_linearYdrift_A0.05_M_space15.0_M_time3.0_beta0.1_delta_space0.005_delta_time0.01_iter_number6_kappa3.0_m0.1_num_MC_path100000_sigma2.0_x_02.0",
                     'rb')
    tmp = pickle.load(file_handler)
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 10))
    plt.suptitle("convergence of outputs from each iteration",
            y=0.95, size=18)
    iteration_figure(tmp, 
                 [0,1,2,3,-2,-1],
                 figure_ax=ax1,
                 x_array_limit=3,
                 xlabel="time",
                 ylabel="function value",
                 other=ax1.plot(np.arange(0,3,0.01),
                        trading_linear_theo(x_0=2,
                        m=0.1,
                        A=0.1,
                        kappa=3,
                        beta=0.1,
                        t_space=np.arange(0,3,0.01)), "--",
                        label="linearization result"))
    iteration_difference_figure(tmp, 
                            [0,1,2,3,-2],
                            figure_ax=ax2,
                            x_array_limit=3,
                            xlabel="time",
                            ylabel="difference from final output",
                            other=ax2.plot(np.arange(0,3,0.01),
                        np.zeros(len(np.arange(0,3,0.01))), "black"))
    
    plt.savefig("trading_iteration_figure.png")
    
    
    
    
    
def trading_iteration_figure3():
    #file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" + 
    #                "model_type_expXdrift_linearYdrift_A0.1_M_space10.0_M_time3.0_beta0.1_delta_space0.005_delta_time0.01_iter_number6_kappa3.0_m0.1_num_MC_path100000_sigma2.0_x_02.0",
    #                'rb')
    file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" +                  
                     "new2/model_type_expXdrift_linearYdrift_A0.25_M_space10.0_M_time2.0_beta0.7_delta_space0.005_delta_time0.01_iter_number15_kappa3.0_m0.15_num_MC_path100000_sigma1.0_x_00.5",
                     'rb')
    tmp = pickle.load(file_handler)
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 10))
    plt.suptitle("convergence of outputs from each iteration",
            y=0.95, size=18)
    iteration_figure(tmp, 
                 [0,1,2,3,-2,-1],
                 figure_ax=ax1,
                 x_array_limit=2,
                 xlabel="time",
                 ylabel="function value",
                 other=ax1.plot(np.arange(0,2,0.01),
                        trading_linear_theo(x_0=0.5,
                        m=0.15,
                        A=0.25,
                        kappa=3,
                        beta=0.7,
                        t_space=np.arange(0,2,0.01)), "--",
                        label="linearization result"))
    iteration_difference_figure(tmp, 
                            [0,1,2,3,-2],
                            figure_ax=ax2,
                            x_array_limit=2,
                            xlabel="time",
                            ylabel="difference from final output",
                            other=ax2.plot(np.arange(0,2,0.01),
                        np.zeros(len(np.arange(0,2,0.01))), "black"))
    
    plt.savefig("trading_iteration_figure.png")
def compare_nonlinear_with_theo():
    file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" + 
                    "model_type_expXdrift_linearYdrift_A0.05_M_space10.0_M_time3.0_beta0.2_delta_space0.005_delta_time0.01_iter_number8_kappa1.6_m0.2_num_MC_path100000_sigma3.0_x_03.0",
                    'rb')
    tmp = pickle.load(file_handler)
    plt.plot(np.arange(0,3,0.01), tmp[-1][:-1], 'g', label="$EY_t$ in iteration 8")
    plt.plot(np.arange(0,3,0.01),
         trading_exp_theo(y_0=tmp[-1][0],
                          beta=0.2,
                          t_space=np.arange(0,3,0.01)), 'r--', label="theoretical exponential function")
    plt.plot(np.arange(0,3,0.01),
         trading_linear_theo(x_0=3,
                        m=0.2,
                        A=0.05,
                        kappa=1.6,
                        beta=0.2,
                        t_space=np.arange(0,3,0.01)), 
        label="linearization result")

    plt.ylabel("function value")
    plt.xlabel("time")
    plt.legend(loc="best")
    plt.title("Comparison between the numerical result "
          +"and the theoretical exponential function")
    
    plt.savefig("nonlinear_convergence_theory.png")
    
def compare_nonlinear_with_theo2():
    #file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" + 
    #                "model_type_expXdrift_linearYdrift_A0.1_M_space15.0_M_time3.0_beta0.1_delta_space0.005_delta_time0.01_iter_number3_kappa0.1_m0.1_num_MC_path10000_sigma2.0_x_02.0",
    #                'rb')
    
    file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" + 
                    "model_type_expXdrift_linearYdrift_A0.05_M_space15.0_M_time3.0_beta0.1_delta_space0.005_delta_time0.01_iter_number6_kappa0.1_m0.1_num_MC_path100000_sigma2.0_x_02.0",
                    'rb')
    tmp = pickle.load(file_handler)
    plt.plot(np.arange(0,3,0.01), tmp[0][:-1], 'r--', label="$EY_t$ in iteration 1")
    plt.plot(np.arange(0,3,0.01), tmp[-1][:-1], 'g', label="$EY_t$ in last iteration")

    plt.plot(np.arange(0,3,0.01),
         trading_linear_theo(x_0=2,
                        m=0.1,
                        A=0.1,
                        kappa=0.1,
                        beta=0.1,
                        t_space=np.arange(0,3,0.01)), 
             "--",
        label="linearization result")

    plt.ylabel("function value")
    plt.xlabel("time")
    plt.legend(loc="best")
    plt.title("Comparison between the numerical result "
          +"and the theoretical exponential function")
    
    plt.savefig("nonlinear_convergence_theory.png")
    
    
def compare_nonlinear_with_theo3():
    #file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" + 
    #                "model_type_expXdrift_linearYdrift_A0.1_M_space15.0_M_time3.0_beta0.1_delta_space0.005_delta_time0.01_iter_number3_kappa0.1_m0.1_num_MC_path10000_sigma2.0_x_02.0",
    #                'rb')
    
    file_handler = open("simulation_result/FBSDE_expXdrift_linarYdrift/" + 
                    "new2/model_type_expXdrift_linearYdrift_A0.25_M_space15.0_M_time2.0_beta0.7_delta_space0.005_delta_time0.01_iter_number5_kappa0.1_m0.15_num_MC_path100000_sigma1.0_x_00.5",
                    'rb')
    tmp = pickle.load(file_handler)

    plt.plot(np.arange(0,2,0.01), tmp[0][:-1], 'r', label="$EY_t$ in iteration 1")

    plt.plot(np.arange(0,2,0.01),
         trading_linear_theo(x_0=0.5,
                        m=0.15,
                        A=0.25,
                        kappa=0.1,
                        beta=0.7,
                        t_space=np.arange(0,2,0.01)), 
             "--",
        label="linearization result")

    plt.ylabel("function value")
    plt.xlabel("time")
    plt.legend(loc="best")
    plt.title("Comparison between the numerical result "
          +"and the theoretical exponential function")
    
    plt.savefig("nonlinear_convergence_theory.png")
    
def compare_g3_with_theo():
    def G3_theo(t_space = np.arange(0, 1, 0.01)):
        y_T = 0.529
        return (y_T ** (-2) + 2 * (1 - t_space)) ** (-0.5)
    
    file_handler = open("simulation_result/G3Ydrift/" +
                    "model_type_G3Ydrift_M_space8.0_M_time1.0_delta_space0.005_delta_time0.01_iter_number10_num_MC_path100000_sigma2.0" ,
                    'rb')
    tmp = pickle.load(file_handler)
    time_array = np.linspace(0, 1, len(G3_theo()))
    plt.plot(time_array, G3_theo(), label="theoretical solution")
    plt.plot(time_array, tmp[8][:-1], 'r--', label="numerical result")
    plt.legend(loc="best")
    plt.ylabel("function value")
    plt.xlabel("time t")
    plt.title("Comparison between the numerical result "
          +"and the theoretical function")
    plt.savefig("g3_convergence_theory.png")
    
def g3_iteration_figure():
    file_handler = open("simulation_result/G3Ydrift/" +
                    "model_type_G3Ydrift_M_space8.0_M_time1.0_delta_space0.005_delta_time0.01_iter_number10_num_MC_path100000_sigma2.0" ,
                    'rb')
    tmp = pickle.load(file_handler)
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 12))
    time_array = np.linspace(0,1,len(tmp[0]))
    arr_list = [0,1,2,3,7,8]
    for i in arr_list:
        ax1.plot(time_array, tmp[i], label="iteration "  + str(i+1))
    
    ax1.legend(loc="best")
    ax1.set_xlabel("time t")
    ax1.set_ylabel("function value")
    
    
    for i in arr_list[:-1]:
        ax2.plot(time_array, tmp[i] - tmp[8], label="iteration " + str(i+1))
    ax2.legend(loc="best")
    ax2.set_xlabel("time t")
    ax2.set_ylabel("difference from final output")
    plt.suptitle("convergence of outputs from each iteration",
                y=0.95, size=18)
    plt.savefig("g3_iteration_figure.png")
if __name__ == '__main__':
    
    #trading_iteration_figure3()
    compare_nonlinear_with_theo3()
    #compare_g3_with_theo()
    #g3_iteration_figure()   