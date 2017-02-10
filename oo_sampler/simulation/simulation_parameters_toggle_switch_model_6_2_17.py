# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 09:26:07 2017

@author: alex
Simulation started on friday 15:45 20.1.2017
"""
import numpy as np
import sys
import ipdb as pdb


sys.path.append("/home/alex/python_programming/ABC/oo_sampler/class_method_smc")
sys.path.append("/home/alex/python_programming/ABC/oo_sampler/functions/help_functions")
sys.path.append("/home/alex/python_programming/ABC/oo_sampler/functions/mixture_model")
import gaussian_densities_etc
#import functions_tuberculosis_model as functions_model
import functions_mixture_model as functions_model


Time = 60
repetitions = 1
dim_particles = 7
target_ESS_ratio_resampler = 0.4
target_ESS_ratio_reweighter = 0.4
epsilon_target = functions_model.epsilon_target(dim_particles)
kwargs = {'N_particles_list': [1000, 1500, 2000, 3000, 4000], # 500,750, , 2500, 3000, 4000, 5000], #[100,200,300,400,500,750,1000], #[1500, 2000, 2500, 3000, 4000, 5000],
            'model_description' : functions_model.model_string,
            'dim_particles' : dim_particles,
            'Time' : Time,
            'dim_auxiliary_var' : 10,
            'augment_M' : True,
            'target_ESS_ratio_reweighter' : target_ESS_ratio_resampler,
            'target_ESS_ratio_resampler' : target_ESS_ratio_reweighter,
            'epsilon_target' : epsilon_target,
            'contracting_AIS' : False,
            'M_increase_until_acceptance' : True,
            'M_target_multiple_N' : 1,
            'covar_factor' : 1.5,
            'propagation_mechanism' : 'AIS',
            'sampler_type' : 'RQMC',
            'ancestor_sampling' : False, #"Hilbert",
            'resample' : True, #True,
            'autochoose_eps' : 'ess_based',
            'save':True,
            'mixture_components' : 10,
            'y_star' : functions_model.f_y_star(dim_particles),
            'epsilon': np.linspace(1, epsilon_target, Time),
            'kernel' : gaussian_densities_etc.gaussian_kernel,
            'move_particle' : gaussian_densities_etc.gaussian_move,
            'inititation_particles' : functions_model.theta_sampler_rqmc,
            'simulator' : functions_model.simulator,
            'delta' : functions_model.delta,
            'exclude_theta' : functions_model.exclude_theta,
            }

K_repetitions = range(repetitions)
filename = functions_model.model_string+'_adaptive_M_autochoose_eps_gaussian_kernel'

if __name__ == '__main__':
    import parallel_simulation
    from functools import partial

    path = "/home/alex/python_programming/ABC_results_storage/simulation_results"
    import os
    os.chdir(path)
    filenames_list = [filename+str(k) for k in K_repetitions]
    partial_parallel_smc = partial(parallel_simulation.set_up_parallel_abc_sampler, **kwargs)
    #partial_parallel_smc(filenames_list[0])
    #partial_parallel_smc(filenames_list[1])
    #parallel_simulation.parmap(partial_parallel_smc,filenames_list)
    for i_simulation in filenames_list:
        partial_parallel_smc(i_simulation)

    # simulation for MC sampler
    kwargs['inititation_particles'] = functions_model.theta_sampler_mc
    kwargs['sampler_type'] = 'MC'
    #pdb.set_trace()

    del partial_parallel_smc
    partial_parallel_smc = partial(parallel_simulation.set_up_parallel_abc_sampler, **kwargs)
    for i_simulation in filenames_list:
        partial_parallel_smc(i_simulation)

    # simulation Del Moral
    kwargs['inititation_particles'] = functions_model.theta_sampler_mc
    kwargs['sampler_type'] = 'MC'
    kwargs['kernel'] = gaussian_densities_etc.uniform_kernel
    kwargs['propagation_mechanism'] = 'Del_Moral'
    kwargs['M_increase_until_acceptance'] = False
    kwargs['augment_M'] = False
    kwargs['covar_factor'] = 2

    del partial_parallel_smc
    partial_parallel_smc = partial(parallel_simulation.set_up_parallel_abc_sampler, **kwargs)
    for i_simulation in filenames_list:
        partial_parallel_smc(i_simulation)

    # simulation Sisson
    kwargs['propagation_mechanism'] = 'true_sisson'
    kwargs['autochoose_eps'] = ''
    kwargs['dim_auxiliary_var'] = 1
    kwargs['epsilon'] =  np.linspace(100, epsilon_target, Time),
    
    del partial_parallel_smc
    partial_parallel_smc = partial(parallel_simulation.set_up_parallel_abc_sampler, **kwargs)
    for i_simulation in filenames_list:
        partial_parallel_smc(i_simulation)