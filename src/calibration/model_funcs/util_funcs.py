'''
UTILITY FUNCTIONS FOR THE SMA-REACT TOOL

All functions are presented in semi-chronological order. 
'''
from math import exp
from numpy import sign
import numpy as np
import time
from scipy.spatial import minkowski_distance
from scipy.spatial.distance import directed_hausdorff
import matplotlib
import matplotlib.pyplot as plt

class DynamicUpdate():
    '''
    Class to define dynamically updating plots in pyqt5
    
    '''
    #Suppose we know the x range


    def on_launch(self,x_data,y_data,numExps):
        '''
        Launching function

        Parameters
        ----------
        x_data : np array
            x data series
        y_data : np array
            y data series
        numExps : int
            number of experiments being analyzed

        Returns
        -------
        None.

        '''
        #Set up plot
        self.figure, self.ax = plt.subplots()
        
        self.exp, = self.ax.plot(x_data,y_data,'bo')
        self.lines = [self.ax.plot([],[], 'r-')[0] for _ in range(numExps)]
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlabel('Temperature, K')
        self.ax.set_ylabel('Strain, mm/mm')
        #self.ax.set_xlim(self.min_x, self.max_x)
        #Other stuff
        self.ax.grid()
        ...

    def on_running(self, xdata, ydata,numExps):
        '''
        Updating function

        Parameters
        ----------
        x_data : np array
            x data series
        y_data : np array
            y data series
        numExps : int
            number of experiments being analyzed

        Returns
        -------
        None.

        '''
        #Update data (with the new _and_ the old points)
        # print(numExps)
        for i in range(numExps):
            self.lines[i].set_xdata(xdata[i])
            self.lines[i].set_ydata(ydata[i])
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    #Example
    def __call__(self):
        '''
        Calling function (example)

        Returns
        -------
        xdata : np array
            example x data
        ydata : np array
            example y data

        '''
        self.on_launch()
        xdata = []
        ydata = []
        for x in np.arange(0,10,0.5):
            xdata.append(x)
            ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
            self.on_running(xdata, ydata)
            time.sleep(1)
        return xdata, ydata


def plot_settings(format_flag):
    '''
    Settings for easy generation of pretty plots. 
    
    Parameters
    ----------
    format_flag : STR
        Options: 'presentation' or 'publication'.
        Presentation makes figures with franklin gothic medium
        Publication makes figures with times new roman

    Returns
    -------
    None.

    '''
    matplotlib.rcParams['svg.fonttype'] = 'none'
    
    # Define available fonts for fallback
    fallback_sans = ["Franklin Gothic Medium", "Arial", "DejaVu Sans", "Liberation Sans"]
    fallback_serif = ["Times New Roman", "DejaVu Serif", "Liberation Serif"]

    if format_flag == "presentation":
        #matplotlib.rcParams["text.usetex"] = False
        matplotlib.rcParams.update({'font.size': 18})
        matplotlib.rcParams["font.sans-serif"] = fallback_sans
        matplotlib.rcParams["font.family"] = "sans-serif"
    elif format_flag == "publication":
        #matplotlib.rcParams["text.usetex"] = True
        matplotlib.rcParams["font.serif"] = fallback_serif
        matplotlib.rcParams["font.family"] = "serif"
        
    return 


def minkowski_error(experiment,model,order=2):
    '''
    Calculate the raw minkowski error between training and testing data.
    

    Parameters
    ----------
    experiment : LIST
        strain-temperature data for the experiment 
    model : LIST
        strain-temperature data for the model prediction
    order : INT, optional
        Order of the minkowski distance. The default is 2.

    Returns
    -------
    minkowski_distance : FLT
        Minkowski distance between experiment and model

    '''
    return minkowski_distance(experiment,model,p=order)

def symmetric_hausdorff(experiment,model):
    '''
    Calculate the general (symmetric) Hausdorff distance between two
    2-D arrays of coordinates

    Parameters
    ----------
    experiment : LIST
        strain-temperature data for the experiment 
    model : LIST
        strain-temperature data for the model prediction

    Returns
    -------
    None.

    '''
    return max(directed_hausdorff(experiment, model)[0], directed_hausdorff(model, experiment)[0])
    



def H_cursolver( sigma, sigma_crit, k, H_min, H_sat):
    '''
    Function to determine the current transformation strain H^cur using
    inputs for stress, critical stress, k, Hsat and Hmin.

    Parameters
    ----------
    sigma : FLT
        current material stress
    sigma_crit : FLT
        critical stress at which transformation strain initiates.
    k : FLT
        coefficient that governs the evolution of transformation 
        strain with respect to applied stress. For more information, 
        see :cite:p:`lagoudas_constitutive_2012`, eq. 3.7 (DOI: https://doi.org/10.1016/j.ijplas.2011.10.009)
    H_min : FLT
        minimium transformation strain
    H_sat : FLT
        maximum, or saturated transformation strain

    Returns
    -------
    H_cur : FLT
        current available transformation strain

    '''

    if abs(sigma) <= sigma_crit:
        H_cur=H_min
    else:
        H_cur = H_min + (H_sat - H_min)*(1-exp(-k*(abs(sigma)-sigma_crit)))

    return H_cur


def partial_Hcur_sigma( sigma, sigma_crit, k, Hsat, Hmin ):
    '''
    Function to solve for the partial derivative of the current
    transformation strain (Hcur) with respect to sigma (stress)    

    Parameters
    ----------
    sigma : FLT
        current material stress
    sigma_crit : FLT
        critical stress at which transformation strain initiates.
    k : FLT
        coefficient that governs the evolution of transformation 
        strain with respect to applied stress. For more information, 
        see :cite:p:`lagoudas_constitutive_2012`, eq. 3.7 (DOI: https://doi.org/10.1016/j.ijplas.2011.10.009)
    H_min : FLT
        minimium transformation strain
    H_sat : FLT
        maximum, or saturated transformation strain

    Returns
    -------
    partial_Hcur_sigma : FLT
        Partial derivative of the current transformation strain with respect
        to current applied stress. 
    '''
    # first solve for the partial derivative of abs(sigma) with respect to sigma
    if sigma > 0:
        partial_abssigma = 1
    elif sigma < 0:
        partial_abssigma = -1
    else:
        partial_abssigma = 0


    # Solve for partial derivative of current transformation strain
    if abs(sigma) <= sigma_crit:
        partial_Hcur_sigma = 0
    else:
        partial_Hcur_sigma = k*(Hsat-Hmin)*exp(-k*(abs(sigma)-sigma_crit))*partial_abssigma

    return partial_Hcur_sigma


def Elastic_Transformation_check_stress( P,TP,sigma, eps_prev, T, T_prev, T0, \
                                        sigma_prev, Phi_fwd_prev, Phi_rev_prev,\
                                        E, MVF, eps_t, eps_t_r, MVF_r ):
    '''
    Function to return Elastic prediction and also check for transformation
    without using scaled projections (non-transformation surface rate-informed)
    
    Returns chck=1 for forward transformation, 2 for reverse transformation 
    and 0 for no transformation
    

    Parameters
    ----------
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations
    sigma : FLT
        Current stress
    eps_prev : FLT
        Previous total strain
    T : FLT
        Current temperature
    T_prev : FLT
        Previous temperature
    T0 : FLT
        Initial temperature
    sigma_prev : FLT
        Previous stress
    Phi_fwd_prev : FLT
        Forward transformation function value for the previous increment
    Phi_rev_prev : FLT
        Reverse transformation function value for the previous increment
    E : FLT
        Youngs modulus
    MVF : FLT
        Current value for martensitic volume fraction
    eps_t : FLT
        Current value for transformation strain
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal

    Returns
    -------
    eps : FLT
        Current total strain
    eps_t : FLT
        Current transformation strain
    MVF : FLT
        Current martensitic volume fraction
    H_cur : FLT
        Current maximum transformation strain
    Phi_fwd : FLT
        Current Forward transformation function value
    Phi_rev : FLT
        Current Reverse transformation function value
    chck : INT
        Flag to describe if transformation is occuring, and in what direction.
        chck=1 for forward transformation (A->M)
             2 for reverse transformation (M->A)
             0 for no transformation (Elastic)
    '''

    # Solve for strain using elastic prediciton
    eps=sigma/E+P['alpha']*(T-T0)+eps_t
    
    #  Solve for current transformational strain
    H_cur=H_cursolver(sigma,P['sig_crit'],P['k'],P['H_min'],P['H_sat'])
    
    # Solve for hardening functions 
    f_fwd = .5*TP['a1']*(1+MVF**P['n_1']-(1-MVF)**P['n_2'])+TP['a3']
    f_rev = .5*TP['a2']*(1+MVF**P['n_3']-(1-MVF)**P['n_4'])-TP['a3']
    
    # Solve for the forward transformation surface
    chck=0
    Phi_fwd = (1-TP['D'])*abs(sigma)*H_cur+\
              .5*(1/P['E_M']-1/P['E_A'])*sigma**2+\
              TP['rho_delta_s0']*T-TP['rho_delta_u0']-f_fwd-TP['Y_0_t']
    # If the forward transformation surface is greater than zero the material
    # is undergoing a forward transformation (chck=1)
    if Phi_fwd >0:
        chck=1
    
    # Solve for the reverse transformation surface
    Phi_rev=0
    
    if MVF_r == 0:
        # Reverse transformation strain remains zero if Martensitic Strain at
        # transformation reversal is zero
        MVR_r = 0
        
    else:
        Phi_rev = -(1+TP['D'])*sigma*eps_t_r/MVF_r-\
                 0.5*(1/P['E_M']-1/P['E_A'])*sigma**2-\
                 TP['rho_delta_s0']*T+TP['rho_delta_u0']+f_rev-TP['Y_0_t']
        # If the revverse transformation surface is greater than zero the material
        # is undergoing a forward transformation (chck=2)
        if Phi_rev > 0:
            chck=2
    return eps, eps_t, MVF, H_cur, Phi_fwd,Phi_rev, chck



def Elastic_Transformation_check_RI_stress( P, TP, sigma, eps_prev, T, T_prev, T0, \
                                           sigma_prev, Phi_fwd_prev, Phi_rev_prev, \
                                               E, MVF, eps_t, eps_t_r, MVF_r ):
    '''
    Function to return elastic prediction and check for transformation using
    scaled elastic projections (transformation surface rate-informed)
    
    Returns chck=1 for forward transformation, 2 for reverse transformation 
    and 0 for no transformation

    Parameters
    ----------
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations
    sigma : FLT
        Current stress
    eps_prev : FLT
        Previous total strain
    T : FLT
        Current temperature
    T_prev : FLT
        Previous temperature
    T0 : FLT
        Initial temperature
    sigma_prev : FLT
        Previous stress
    Phi_fwd_prev : FLT
        Forward transformation function value for the previous increment
    Phi_rev_prev : FLT
        Reverse transformation function value for the previous increment
    E : FLT
        Youngs modulus
    MVF : FLT
        Current value for martensitic volume fraction
    eps_t : FLT
        Current value for transformation strain
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal

    Returns
    -------
    eps : FLT
        Current total strain
    eps_t : FLT
        Current transformation strain
    MVF : FLT
        Current martensitic volume fraction
    H_cur : FLT
        Current maximum transformation strain
    Phi_fwd : FLT
        Current Forward transformation function value
    Phi_rev : FLT
        Current Reverse transformation function value
    chck : INT
        Flag to describe if transformation is occuring, and in what direction.
        chck=1 for forward transformation (A->M)
             2 for reverse transformation (M->A)
             0 for no transformation (Elastic)

    '''

    
    # Solve for strain using elastic prediciton
    eps=sigma/E+P['alpha']*(T-T0)+eps_t
    
    # Solve for current transformational strain  
    H_cur=H_cursolver(sigma,P['sig_crit'],P['k'],P['H_min'],P['H_sat'])
    
    # Solve for hardening functions 
    f_fwd = .5*TP['a1']*(1+MVF**P['n_1']-(1-MVF)**P['n_2'])+TP['a3']
    f_rev = .5*TP['a2']*(1+MVF**P['n_3']-(1-MVF)**P['n_4'])-TP['a3']
    
    # Solve for the forward transformation surface
    Phi_fwd = (1-TP['D'])*abs(sigma)*H_cur+.5*(1/P['E_M']-1/P['E_A'])*sigma**2+TP['rho_delta_s0']*T-TP['rho_delta_u0']-f_fwd-TP['Y_0_t']
    
    # Solve for the reverse transformation surface
    Phi_rev=0
    if MVF_r == 0:
        MVR_r =0
        # Reverse transformation strain remains zero if Martensitic Strain at
        # transformation reversal is zero
    else:
        Phi_rev = -(1+TP['D'])*sigma*eps_t_r/MVF_r-.5*(1/P['E_M']-1/P['E_A'])*sigma**2-TP['rho_delta_s0']*T+TP['rho_delta_u0']+f_rev-TP['Y_0_t']
    
    # Find the scaled projections of strain, temperature (and the scaled change
    # (delta) in these values
    # s: scaling factor
    s = 0.001
    scaled_d_eps = s*(eps - eps_prev)
    scaled_d_T = s*(T - T_prev)
    scaled_T = scaled_d_T + T_prev
    
    # Find the scaled projection of stress using scaled projections for strain
    # and temperature
    scaled_d_sigma= E*((eps_prev+scaled_d_eps) - P['alpha']*(scaled_T - T0) - eps_t) - sigma_prev
    scaled_sigma= scaled_d_sigma + sigma_prev
    
    # Calculate the scaled projections for forward and reverse transformation
    # surface
    # Calculate the current transformational strain for these scaled values
    # (required to find the transformation surfaces)
    scaled_H_cur = H_cursolver(scaled_sigma,P['sig_crit'],P['k'],P['H_min'],P['H_sat'])
    # Forward transformation surface for scaled values
    scaled_Phi_fwd = (1-TP['D'])*abs(scaled_sigma)*scaled_H_cur+.5*(1/P['E_M']-1/P['E_A'])*scaled_sigma**2+TP['rho_delta_s0']*scaled_T - TP['rho_delta_u0'] - f_fwd - TP['Y_0_t']
    # Reverse transformation surface for scaled values
    scaled_Phi_rev=0
    if MVF_r == 0:
        MVR_r =0
    else:
        scaled_Phi_rev = -(1+TP['D'])*scaled_sigma*eps_t_r/MVF_r - .5*(1/P['E_M']-1/P['E_A'])*scaled_sigma**2 - TP['rho_delta_s0']*scaled_T + TP['rho_delta_u0']+f_rev-TP['Y_0_t']
    
    
    # Check for transformation
    # Determine change in transformation surface from the previous value to the
    # scaled projection
    scaled_d_Phi_fwd = scaled_Phi_fwd - Phi_fwd_prev
    scaled_d_Phi_rev = scaled_Phi_rev - Phi_rev_prev
    
    # Forward Transformation Check
    if scaled_d_Phi_fwd > 0 and scaled_d_Phi_rev <= 0:
        if Phi_fwd > 0 and MVF < 1:
            # Forward transformation
            chck = 1
        else:
            # No transformation
            chck = 0
    # Reverse transformation check    
    elif scaled_d_Phi_rev > 0 and scaled_d_Phi_fwd <= 0:
        if Phi_rev > 0 and MVF > 0:
            # Reverse transformation
            chck = 2
        else:
            #No transformation
            chck = 0
        
    elif scaled_d_Phi_rev <= 0 and scaled_d_Phi_fwd <=0:
        # No transformation
        chck = 0
        
    elif scaled_d_Phi_fwd > 0 and scaled_d_Phi_rev > 0:
        if Phi_fwd <= 0 and Phi_rev <=0:
            #No transformation
            chck = 0
        elif Phi_fwd > 0 and Phi_rev <= 0:
            # Check for forward transformation
            if Phi_fwd > 0 and MVF < 1:
                # Forward transformation
                chck = 1
            else:
                # No transformation
                chck = 0
        
        elif Phi_rev > 0 and Phi_fwd <= 0:
            # Check for reverse transformation
            if Phi_rev > 0 and MVF > 0:
                # Reverse transformation
                chck = 2
            else:
                #No transformation
                chck = 0
        # If both transformation surfaces are greater than zero, check which one
        # has the higher rate of change
        elif Phi_fwd > 0 and Phi_rev > 0:
            if scaled_d_Phi_fwd > scaled_d_Phi_rev:
                # Check for forward transformation
                if Phi_fwd > 0 and MVF < 1:
                    # Forward transformation
                    chck = 1
                else:
                    # No transformation
                    chck = 0
            
            else:
                # Check for reverse transformation
                if Phi_rev > 0 and MVF > 0:
                    # Reverse transformation
                    chck = 2
                else:
                    #No transformation
                    chck = 0

    #chck
    return eps, eps_t, MVF, H_cur, Phi_fwd, Phi_rev, chck


def Explicit_Transformation_Correction_stress( P, TP, chck,MVF, eps_t, E,\
                                              MVF_r,eps_t_r,sigma, H_cur,eps,\
                                                  T, T_0, Phi_fwd, Phi_rev ):
    '''
    Function to return the outputs for Martensitic volume fraction, stress,
    transformation strain, Young's modulus, etc. using explicit integration
    scheme. Input variables are from elastic prediction.

    Parameters
    ----------
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations
    chck : INT
        Flag to describe if transformation is occuring, and in what direction.
        chck=1 for forward transformation (A->M)
             2 for reverse transformation (M->A)
             0 for no transformation (Elastic)
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    sigma : FLT
        Current stress
    H_cur : FLT
        Current maximum transformation strain
    eps : FLT
        Current total strain
    T : FLT
        Current temperature
    T0 : FLT
        Initial temperature
    Phi_fwd : FLT
        Current Forward transformation function value
    Phi_rev : FLT
        Current Reverse transformation function value

    Returns
    -------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    eps : FLT
        Current total strain
    Phi_fwd : FLT
        Current Forward transformation function value
    Phi_rev : FLT
        Current Reverse transformation function value

    '''

    
    # Return elastic predictions if no transformation is occuring
    if chck == 0:
        return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd, Phi_rev
     
    # Forward Transformation correction    
    if chck ==1:
        (MVF, eps_t, E, MVF_r,    \
         eps_t_r, eps, Phi_fwd) = \
            Explicit_fwd_transformation_correction_stress( \
                        MVF, eps_t, sigma, H_cur,eps, T, T_0,P,TP )
        
    # Reverse Transformation correction    
    elif chck == 2:
        (MVF, eps_t, E, MVF_r,     \
         eps_t_r, eps, Phi_rev ) = \
            Explicit_rev_transformation_correction_stress( \
                MVF, eps_t, MVF_r,eps_t_r,sigma, eps, T, T_0,P, TP )
    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd, Phi_rev

def Explicit_fwd_transformation_correction_stress( MVF, eps_t, sigma, H_cur,eps, T, T_0,P, TP ):
    '''
    Function to correct for forward transformation using explicit integration scheme
    Input variables are from elastic prediction

    Parameters
    ----------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    sigma : FLT
        Current stress
    H_cur : FLT
        Current maximum transformation strain
    eps : FLT
        Current total strain
    T : FLT
        Current temperature
    T0 : FLT
        Initial temperature
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations

    Returns
    -------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    eps : FLT
        Current total strain
    Phi_fwd : FLT
        Current Forward transformation function value

    '''
    # P: Material Properties
    # TP: Transformation Properties

    # Calculate forward hardening function
    f_fwd=(1-TP['D'])*abs(sigma)*H_cur+.5*(1/P['E_M']-1/P['E_A'])*sigma**2+TP['rho_delta_s0']*T-TP['rho_delta_u0']-TP['Y_0_t']

    # Solve for corrected MVF (explicit formula only works for n1=n2=n3=n4=1)
    # Hold values of MVF from previous load to for calculation of eps_t 
    MVF_previous=MVF
    MVF=(f_fwd-TP['a3'])/TP['a1']
    # Correct if MVF bounds violated
    if MVF > 1:
        MVF = 1

    # Solve for transformation direction
    lamda = H_cur*sign(sigma)

    # Solve for transformation strain
    eps_t=eps_t+(MVF-MVF_previous)*lamda
    # Update transformation strain and martensitic volume fraction at transformation reversal
    eps_t_r=eps_t
    MVF_r=MVF

    # Update Output Variables
    # Solve for Young's Modulus
    E = 1.0/(1.0/P['E_A'] + MVF*(1/P['E_M'] - 1/P['E_A']))
    # E= inv(inv(P['E_A'])+MVF*(inv(P['E_M'])-inv(P['E_A'])))
    # Solve for Strain
    eps=sigma/E+P['alpha']*(T-T_0)+eps_t

    # Update the forward transformation surface
    Phi_fwd = (1-TP['D'])*abs(sigma)*H_cur+.5*(1/P['E_M']-1/P['E_A'])*sigma**2+TP['rho_delta_s0']*T-TP['rho_delta_u0']-f_fwd-TP['Y_0_t']

    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd

def Explicit_rev_transformation_correction_stress( MVF, eps_t, MVF_r,eps_t_r,sigma, eps, T, T_0,P, TP ):
    '''
    Function to correct for reverse transformation using implicit integration scheme
    Input variables are from elastic prediction

    Parameters
    ----------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    sigma : FLT
        Current stress
    eps : FLT
        Current total strain
    T : FLT
        Current temperature
    T0 : FLT
        Initial temperature
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations

    Returns
    -------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    eps : FLT
        Current total strain
    Phi_rev : FLT
        Current Reverse transformation function value

    '''
    # Calculate reverse hardening function
    f_rev=-(-(1+TP['D'])*sigma*eps_t_r/MVF_r-.5*(1/P['E_M']-1/P['E_A'])*sigma**2-TP['rho_delta_s0']*T+TP['rho_delta_u0']-TP['Y_0_t'])

    # Hold values of MVF from previous load to for calculation of eps_t 
    MVF_previous=MVF
    # Solve for corrected MVF (explicit formula only works for n1=n2=n3=n4=1)
    MVF=(f_rev+TP['a3'])/TP['a2']
    # Correct if MVF bounds violated
    if MVF < 0:
        MVF = 0

    # Solve for Transformation Direction
    lamda = eps_t_r/MVF_r

    # Solve for transformation strain
    eps_t=eps_t+(MVF-MVF_previous)*lamda
    # eps_t_r does not change

    # Update transformation strain and martensitic volume fraction at transformation reversal
    if MVF == 0:
        MVF_r = 0
        eps_t_r = 0


    # Update Output Variables
    # Solve for Young's Modulus
    E = (1/P['E_A']+MVF*(1/P['E_M']-1/P['E_A']))**-1
    # Solve for Strain
    eps=sigma/E+P['alpha']*(T-T_0)+eps_t

    # Solve for the reverse transformation surface
    Phi_rev=0
    if MVF_r == 0:
        # Reverse transformation strain remains zero if Martensitic Strain at transformation reversal is zero
        Phi_rev=0

    else:
        Phi_rev = -(1+TP['D'])*sigma*eps_t_r/MVF_r-.5*(1/P['E_M']-1/P['E_A'])*sigma**2-TP['rho_delta_s0']*T+TP['rho_delta_u0']+f_rev-TP['Y_0_t']

    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_rev

def Implicit_Transformation_Correction_stress( P, TP, chck,MVF, eps_t, E,\
                                              MVF_r,eps_t_r,sigma, H_cur,\
                                                  eps, T, T_0, Phi_fwd, Phi_rev ):
    '''
    Function to return the outputs for Martensitic volume fraction, stress,
    transformation strain, Young's modulus, etc. using implicit integration
    scheme. Input variables are from elastic prediction

    Parameters
    ----------
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations
    chck : INT
        Flag to describe if transformation is occuring, and in what direction.
        chck=1 for forward transformation (A->M)
             2 for reverse transformation (M->A)
             0 for no transformation (Elastic)
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    sigma : FLT
        Current stress
    H_cur : FLT
        Current maximum transformation strain
    eps : FLT
        Current total strain
    T : FLT
        Current temperature
    T0 : FLT
        Initial temperature
    Phi_fwd : FLT
        Current Forward transformation function value
    Phi_rev : FLT
        Current Reverse transformation function value

    Returns
    -------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    eps : FLT
        Current total strain
    Phi_fwd : FLT
        Current Forward transformation function value
    Phi_rev : FLT
        Current Reverse transformation function value

    '''

    
    # Return elastic predictions if no transformation is occuring
    if chck==0:
        return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd, Phi_rev

    # Forward transformation correction
    if chck==1:
        
        MVF, eps_t, E, MVF_r,   \
        eps_t_r, eps, Phi_fwd = \
            Implicit_fwd_transformation_correction_stress( \
                MVF, eps_t, E,MVF_r,eps_t_r,sigma, \
                H_cur,eps, T, T_0,Phi_fwd,P,TP )
        
    # Reverse transformation correction    
    elif chck==2:
        MVF, eps_t, E, MVF_r,   \
        eps_t_r, eps, Phi_rev = \
            Implicit_rev_transformation_correction_stress( \
                MVF, eps_t, E,MVF_r,eps_t_r,sigma, \
                eps, T, T_0,Phi_rev,P, TP)
            
    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd, Phi_rev

def Implicit_fwd_transformation_correction_stress( MVF, eps_t, E,MVF_r,eps_t_r,sigma, H_cur,eps, T, T_0, Phi_fwd,P, TP ):
    '''
    Function to correct for forward transformation using implicit integration scheme.
    Input variables are from elastic prediction

    Parameters
    ----------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    sigma : FLT
        Current stress
    H_cur : FLT
        Current maximum transformation strain
    eps : FLT
        Current total strain
    T : FLT
        Current temperature
    T0 : FLT
        Initial temperature
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations

    Raises
    ------
    exception
        Return mapping algorithm failed. 

    Returns
    -------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    eps : FLT
        Current total strain
    Phi_fwd : FLT
        Current Forward transformation function value

    '''

    
    # Find initial values for iteration (k=1)
    # Evaluate transformation direction (Lambda)
    Lambda = H_cur*sign(sigma)
    # Iterate MVF until its change after an iteration is negligible (less than
    # assigned tolerance MVF_tolerance) or until Martensitic volume fraction
    # reaches bound of 1
    maxiter = 1000
    for i in range(maxiter):
        # Determine the partial derivative of the current
        # transformation strain (Hcur) and transformation surface (Phi)
        # with respect to stress using functions for these equations
        partial_Hcur_sigma_k=partial_Hcur_sigma(sigma,P['sig_crit'],P['k'],P['H_sat'],P['H_min'])
        partial_Phi_fwd_sigma_k=partial_Phi_fwd_sigma(sigma,H_cur,TP['D'],partial_Hcur_sigma_k,P['E_M'],P['E_A'])
        
        # Determine the partial derivative of transformation surface
        # (Phi) with respect to Martensitic volume fraction
        partial_Phi_fwd_MVF_k=partial_Phi_fwd_MVF(MVF,P['delta'],P['n_1'],P['n_2'],TP['a1'],TP['a2'],TP['a3'])
        
        # Use partial derivatives and MVF evolution to solve A^t
        A_t=partial_Phi_fwd_MVF_k-partial_Phi_fwd_sigma_k*E*((1/P['E_M']-1/P['E_A'])*sigma+Lambda)
        
        # Determine the correction for MVF for the current iteration
        delta_MVF=-Phi_fwd/partial_Phi_fwd_MVF_k
        
        # Hold the MVF value of the previous iteration in case of
        # MVF > 1 correction
        MVF_k=MVF
        # Update MVF using the delta MVF value
        MVF=MVF+delta_MVF
        
        # Correct if MVF reaches a bound of 1
        if MVF > 1:
            MVF = 1
            # Recalculate transformation strain for corrected MVF
            eps_t=eps_t+(MVF-MVF_k)*Lambda
            # Youngs Modulus for completely martensite material
            E=P['E_M']
            # Update transformation reversal values
            eps_t_r=eps_t
            MVF_r=MVF
            break        
        # Update transformation strain using  calculated values for change in
        # MVF (delta_MVF) and transformation direction
        eps_t=eps_t+delta_MVF*Lambda;
        # Update value for Young's Modulus 
        E=(1/P['E_A']+MVF*(1/P['E_M']-1/P['E_A']))**(-1)
        
        # Update transformation surface/output variables for next
        # iteration using values for current transformation strain,
        # transformation direction and hardening function
        # Update current transformation strain
        H_cur=H_cursolver(sigma,P['sig_crit'],P['k'],P['H_min'],P['H_sat'])
        # Update transformation direction
        Lambda = H_cur*sign(sigma);
        # Update hardeing function
        f_fwd = .5*TP['a1']*(1+(MVF**(1/P['n_1'])/(MVF+P['delta'])**(1/P['n_1']-1))**P['n_1']-((1-MVF)**(1/P['n_2'])/(1-MVF+P['delta'])**(1/P['n_2']-1))**P['n_2'])+TP['a3']
        # Update transformation surface
        Phi_fwd = (1-TP['D'])*abs(sigma)*H_cur+.5*(1/P['E_M']-1/P['E_A'])*sigma**2+TP['rho_delta_s0']*T-TP['rho_delta_u0']-f_fwd-TP['Y_0_t']
        
        # Update transformation reversal values
        eps_t_r=eps_t
        MVF_r=MVF
        
        if abs(delta_MVF) < P['MVF_tolerance']:
            break
        
        if iter == maxiter:
            raise exception(['ERROR: MAXIMUM NUMBER OF ITERATIONS (' +str(iter) + ') REACHED IN THE RMA'])
        
        
    # Update strain (eps) using known values of sigma, T and updated values
    # of E and eps_t
    eps= sigma/E + P['alpha']*(T-T_0)+eps_t
    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd

def Implicit_rev_transformation_correction_stress( MVF, eps_t, E,MVF_r,eps_t_r,sigma, eps, T, T_0, Phi_rev,P, TP):
    '''
    Function to correct for reverse transformation using implicit integration scheme
    Input variables are from elastic prediction/ transformation check

    Parameters
    ----------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    sigma : FLT
        Current stress
    eps : FLT
        Current total strain
    T : FLT
        Current temperature
    T0 : FLT
        Initial temperature
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations

    Raises
    ------
    exception
        Return mapping algorithm failed. 

    Returns
    -------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    eps : FLT
        Current total strain
    Phi_rev : FLT
        Current Reverse transformation function value

    '''
    
    # Find initial values for iteration (k=1)
    # Transformation Direction for reverse transformation
    Lamda = eps_t_r/MVF_r

    # Iterate MVF until its change after an iteration is negligible (less than
    # assigned tolerance MVF_tolerance) or until MVF reaches bound of 0

    maxiter = 100
    for i in range(maxiter):
        
        # Determine the partial derivative of the transformation
        # surface (Phi) with respect to stress
        partial_Phi_rev_sigma_k=-(1+TP['D'])*eps_t_r/MVF_r-(1/P['E_M']-1/P['E_A'])*sigma
        
        # Determine the partial derivative of transformation surface
        # (Phi) with respect to Martensitic volume fraction
        partial_Phi_rev_MVF_k=partial_Phi_rev_MVF(MVF,P['delta'],P['n_3'],P['n_4'],TP['a1'],TP['a2'],TP['a3'])
        
        # Use partial derivatives and MVF evolution to solve A^t
        A_t=partial_Phi_rev_MVF_k-partial_Phi_rev_sigma_k*E*((1/P['E_M']-1/P['E_A'])*sigma+Lamda)
        
        # Determine the correction for MVF for the current iteration
        delta_MVF=-Phi_rev/partial_Phi_rev_MVF_k
        
        # Update MVF using the delta MVF value
        # Hold the MVF value of the previous iteration in case of
        # MVF < 0 correction
        MVF_k=MVF
        MVF=MVF+delta_MVF
        
        # Correct if MVF reaches a bound of 0
        if MVF < 0:
            MVF = 0
            # Recalculate transformation strain for corrected MVF
            eps_t=eps_t+(MVF-MVF_k)*Lamda
            # Youngs Modulus for austenite material
            E=P['E_A']
            # Update transformation reversal values to zero
            eps_t_r=0
            MVF_r=0
            break
        
    
        # Update transformation strain using calculated values for change in
        # MVF (delta_MVF) and transformation direction
        eps_t=eps_t+delta_MVF*Lamda
        # Update value for Young's Modulus and use this value to determine
        # stress (sigma)
        
        E=(1/P['E_A']+MVF*(1/P['E_M']-1/P['E_A']))**-1
    
        
        # Update transformation surface/output variables for next
        # iteration
        # Update transformation direction

        Lamda = eps_t_r/MVF_r
        # Update hardening function
        f_rev = .5*TP['a2']*(1+(MVF**(1/P['n_3'])/(MVF+P['delta'])**(1/P['n_3']-1))**P['n_3']-((1-MVF)**(1/P['n_4'])/(1-MVF+P['delta'])**(1/P['n_4']-1))**P['n_4'])-TP['a3']
        # Update transformation surface
        Phi_rev = -(1+TP['D'])*sigma*eps_t_r/MVF_r-.5*(1/P['E_M']-1/P['E_A'])*sigma**2-TP['rho_delta_s0']*T+TP['rho_delta_u0']+f_rev-TP['Y_0_t']
        
        # Transformation reversal values remain the same
        if abs(delta_MVF) < P['MVF_tolerance']:
            break
    
        
        if iter == maxiter:
            raise exception(['ERROR: MAXIMUM NUMBER OF ITERATIONS (' +str(iter) + ') REACHED IN THE RMA'])


    # Update strain (eps) using known values of sigma, T and updated values 
    # of E and eps_t
    eps= sigma/E + P['alpha']*(T-T_0)+eps_t
    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_rev

def partial_Phi_fwd_MVF( MVF, delta, n1, n2,a1,a2,a3 ):
    # Solve for the partial derivative of transformation surfade Phi with
    # respect to the martensitic volume fraction MVF.
    partial_Phi_fwd_MVF=-1/2*(-(1-MVF+delta)**(n2-2)*n2*MVF+MVF*(MVF+delta)**(n1-2)*n1+(1-MVF+delta)**(n2-2)*delta+(1-MVF+delta)**(n2-2)*n2+(MVF+delta)**(n1-2)*delta)*a1
    
    return partial_Phi_fwd_MVF

def partial_Phi_fwd_sigma( sigma, Hcur, D, partial_H_cur_sigma, E_M, E_A ):
    # Solve the partial derivative of forward Transformation Surface (Phi_t) 
    # with respect to stress (sigma)

    if sigma < 0:
        partial_Phi_fwd_t_sigma=-(1-D)*Hcur+(1-D)*abs(sigma)*partial_H_cur_sigma+(1/E_M-1/E_A)*sigma
    elif sigma > 0:
        partial_Phi_fwd_t_sigma=(1-D)*Hcur+(1-D)*abs(sigma)*partial_H_cur_sigma+(1/E_M-1/E_A)*sigma
    else:
        partial_Phi_fwd_t_sigma=0
    return partial_Phi_fwd_t_sigma

def partial_Phi_rev_MVF( MVF, delta, n3, n4,a1,a2,a3 ):
    # Solve for the partial derivative of transformation surfade Phi with
    # respect to the martensitic volume fraction MVF.
    
    partial_Phi_rev_MVF=1/2*(-(1-MVF+delta)**(n4-2)*n4*MVF+MVF*(MVF+delta)**(n3-2)*n3+(1-MVF+delta)**(n4-2)*delta+(1-MVF+delta)**(n4-2)*n4+(MVF+delta)**(n3-2)*delta)*a2
    return partial_Phi_rev_MVF
