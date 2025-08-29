# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:03:57 2024

@author: pwal5
"""

import scipy.io

import numpy as np

import matplotlib.pyplot as plt

import os


def celsius_to_kelvin(temperature):
    return temperature + 273.15 

def kelvin_to_celsius(temperature):
    return temperature - 273.15

'''MATPLOTLIB PRESETS'''
#Graphs in a separate window
get_ipython().run_line_magic('matplotlib', 'qt')
#Graphs inline (ala Jupyter notebook)
#get_ipython().run_line_magic('matplotlib', 'inline')
plt.rc('font', family='serif') 
plt.rc('font', serif='Times New Roman') 
plt.rc('text', usetex='True') 
plt.rcParams.update({'font.size': 10})
plt.rcParams['svg.fonttype'] = 'none'


get_ipython().run_line_magic('matplotlib','qt')

file_name = 'Fig2a_FAT01_429_E195HT_550C3hrAC_T_C_H_LB True 2ndCycle.mat'

mat = scipy.io.loadmat(file_name)

temperature = mat['Xdata_SampTemp_degC']

strain = mat['Ydata_TrueStrain_pct']

colors = mat['LineColors']

stress_levels = [400, 300, 200, 100, 50, 7]
red = [1, 0 , 0]
blue = [0, 0, 1]

fig, ax = plt.subplots(1,1)

data = {}

from savitzky_golay import savitzky_golay
from scipy.interpolate import Akima1DInterpolator, CubicSpline

def resample_data(x_data,y_data,num_points):
    resampled_x_data = np.linspace(min(x_data),max(x_data),num_points)
    
    # Filter based on a Savitzky-Golay 1-D filter
    y_filtered = savitzky_golay(
        y_data,
        window_size=51,
        order=4)
    
    x_filtered = savitzky_golay(
        x_data,
        window_size=51,
        order=4)
    
    
    # defining arbitrary parameter to parameterize the curve
    path_t = np.linspace(0,1,x_filtered.size)
    
    r = np.hstack(
        (x_filtered.reshape((x_filtered.size,1)),
         y_filtered.reshape((y_filtered.size,1))))
    
    # defining values of the arbitrary parameter over which
    # you want to interpolate x and y
    # it MUST be within 0 and 1, since you defined
    # the spline between path_t=0 and path_t=1
    t = np.linspace(np.min(path_t),np.max(path_t),num_points)
    
    cs = CubicSpline(path_t, r)
    
    resampled_data = cs(t)
    
    resampled_x_data = resampled_data[:,0]
    resampled_y_data = resampled_data[:,1]
    
    # plt.plot(resampled_x_data,resampled_y_data,'k.',
    #          x_data,y_data,'b')
    
    
    return resampled_x_data, resampled_y_data


for i in range(int(len(temperature[0,:])/2)):
    heating_temperature = temperature[0,2*i].T
    cooling_temperature = temperature[0,2*i+1].T
    
    heating_strain = strain[0,2*i].T
    cooling_strain = strain[0,2*i+1].T
    
    heating_temperature,heating_strain = resample_data(
        heating_temperature[:,0],
        heating_strain[:,0],
        num_points=200
        )
    
    cooling_temperature, cooling_strain = resample_data(
        cooling_temperature[:,0],
        cooling_strain[:,0],
        num_points = 200
        )
    
    
    
    
    total_temperature = np.concatenate(
        (heating_temperature,cooling_temperature[::-1])
        )
    total_strain = np.concatenate(
        (heating_strain,cooling_strain[::-1])
        )
    total_stress = np.full(
        shape=(len(total_temperature),1),
        fill_value = stress_levels[i]
        )
    
    data = np.zeros((len(total_temperature),3))
    
    data[:,0] = total_temperature
    data[:,1] = total_strain
    data[:,2] = total_stress[:,0]
    
    max_temperature_index = np.argmax(data[:,0])
    max_temperature = np.max(data[:,0])
    elastic_strain = data[max_temperature_index,1]
    elastic_stress = data[max_temperature_index,2]
    
    print('max temp = ',max_temperature)
    print('strain = ', elastic_strain)
    print('stress = ', elastic_stress)
    
    # file_name = str(stress_levels[i])+' MPa.txt'
    
    # np.savetxt(file_name,data,delimiter='\t')
    
    # data['experiment'+str(i)] = {}
    
    # data['experiment'+str(i)]['Temperature'] = total_temperature
    # data['experiment'+str(i)]['Stress'] = total_stress
    # data['experiment'+str(i)]['Strain'] = total_strain
    
    
    
    
    if colors[0,i][0,0] == 1:
        color = 'r'
    elif colors[0,i][0,2] == 1:
        color = 'b'
        
    ax.scatter(
        cooling_temperature,
        cooling_strain,
        label=i,
        color='b',
        s=7.5)
    
    ax.scatter(
        heating_temperature,
        heating_strain,
        color='r',
        s=7.5)
    
    plt.show()
    
    
for i in range(len(stress_levels)):
    file_name = 'optimal_model_'+str(i)+'.csv'
    file_path = os.path.join(
        "C:\\Users\\pwal5\\Documents\\GitHub\\SMAREACTcleaned\\output\\sample_2_estimate",
        file_name
        )
    data = np.loadtxt(file_path,delimiter=',')
    
    max_temperature_index = np.argmax(data[:,0])
    
    model_heating = data[:max_temperature_index,0]-273.15
    model_heating_strain = data[:max_temperature_index,1]*100
    
    model_cooling = data[max_temperature_index:,0]-273.15
    model_cooling_strain = data[max_temperature_index:,1]*100
    
    ax.plot(model_heating,model_heating_strain,'r--')
    ax.plot(model_cooling,model_cooling_strain,'b--')
    
secax_x = ax.secondary_xaxis(
    -0.25, functions=(celsius_to_kelvin, kelvin_to_celsius))
secax_x.set_xlabel('Temperature, K')
    
ax.set_xlabel('Temperature, $^\circ$C')
ax.set_ylabel('Strain, \%')

fig.set_size_inches(6,3.5)

fig.tight_layout()
    


