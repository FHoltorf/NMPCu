#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 21:55:13 2018

@author: flemmingholtorf
"""
from __future__ import print_function
from main.mods.SemiBatchPolymerization.mod_class import SemiBatchPolymerization
from main.dync.MHEGen import MHEGen
from main.examples.SemiBatchPolymerization.noise_characteristics import * 
from scipy.stats import chi2
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# don't write messy bytecode files
# might want to change if ran multiple times for performance increase
# sys.dont_write_bytecode = True 

# discretization parameters:
nfe, ncp = 24, 3 # Radau nodes assumed in code
# state variables:
x_vars = {"PO":[()], "Y":[()], "W":[()], "PO_fed":[()], "MY":[()], "MX":[(0,),(1,)], "T":[()], "T_cw":[()]}
# corrupted state variables:
x_noisy = []
# output variables:
y_vars = {"PO":[()], "Y":[()], "MY":[()], 'T':[()], 'T_cw':[()]}
# controls:
u = ["u1", "u2"]
u_bounds = {"u1": (0.0,0.4), "u2": (0.0, 3.0)} 
# uncertain parameters:
p_noisy = {"A":[('p',),('i',)],'kA':[()]}
# noisy initial conditions:
noisy_ics = {'PO_ic':[()],'T_ic':[()],'MY_ic':[()],'MX_ic':[(1,)]}
# initial uncertainty set description (hyperrectangular):
p_bounds = {('A', ('i',)):(-0.2,0.2),('A', ('p',)):(-0.2,0.2),('kA',()):(-0.2,0.2),
            ('PO_ic',()):(-0.02,0.02),('T_ic',()):(-0.005,0.005),
            ('MY_ic',()):(-0.01,0.01),('MX_ic',(1,)):(-0.002,0.002)}
# time horizon bounds:
tf_bounds = [10.0*24/nfe, 30.0*24/nfe]
# path constrained properties to be monitored:
pc = ['Tad','T']
# monitored vars:
poi = [x for x in x_vars] + u         
            
# create MHE-NMPC-controller object
cl = MHEGen(d_mod = SemiBatchPolymerization,
           y=y_vars,
           x=x_vars,           
           x_noisy=x_noisy,
           p_noisy=p_noisy,
           u=u,
           u_bounds = u_bounds,
           tf_bounds = tf_bounds,
           poi = x_vars,
           noisy_inputs = False,
           noisy_params = True,
           adapt_params = True,
           update_uncertainty_set = False,
           process_noise_model = None,
           obj_type='economic',
           control_displacement_penalty=True,
           nfe_t=nfe,
           ncp_t=ncp,
           path_constraints=pc)

cov_matrices = {'y_cov':mcov,'q_cov':qcov,'u_cov':ucov,'p_cov':pcov}
reg_weights = {'K_w':1.0}
args = {'cov_matrices':cov_matrices, 'regularization_weights':reg_weights,
        'advanced_step':False,'fix_noise':True,'meas_noise':x_measurement,'disturbance_src':{}}

kind = 'NMPC'
parest = '_parest_' if cl.adapt_params else '_'