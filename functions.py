'''Funciones para calculos de caida de presion'''

import numpy as np

def friction_factor(diameter, Re_num, epsilon):
    f_factor_old = 0.02
    error = 1
    max_iter = 1000
    iter = 0

    while (error > 0.000001)&(iter < max_iter):
        f_factor_new = 1 / (-2 * np.log((epsilon / (3.7 * diameter)) + (2.51 / (Re_num * np.sqrt(f_factor_old)))) / np.log(10))** 2
        error = np.abs((f_factor_new - f_factor_old)/f_factor_new)
        f_factor_old = f_factor_new
        iter += 1
    
    return f_factor_new


def reynolds(density, velocity, diameter, viscosity): #Calculo de reynolds unidades: (kg / m3, m / s, m , Pa * s) respectively
    diameter = diameter / 1000
    re_num = density * velocity * diameter / viscosity
    return re_num

def pressure_loss(f_factor, diameter, length, velocity):
    gravity_constant = 9.81
    diameter = diameter / 1000
    hf =  f_factor * (length / diameter) * (velocity ** 2) / (2 * gravity_constant)
    return hf
