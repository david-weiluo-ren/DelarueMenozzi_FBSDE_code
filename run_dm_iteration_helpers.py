'''
Created on Jan 28, 2016

@author: weiluo
'''






def dm_iterate_helper(model_factory, iter_number = 20, *args, **kwargs):
    eta = None
    system = None
    all_etas = [] 
    for i in range(iter_number):
        print("start {i}th iteration".format(i=i))
        if i == 0:
            system = model_factory('init', *args, **kwargs)
        else:
            system = model_factory('use_expectation',
                                   eta = eta, 
                                   *args, 
                                   **kwargs)
        system.compute_all_link()
        system.simulate_forward()
        eta = system.expectation_g_Y
        all_etas.append(eta)
    return all_etas