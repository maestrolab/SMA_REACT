'''
optimizer.py

This script contains all the optimization-specific routines. 
'''
import random
import shelve
import pprint
import os
import sys

import numpy as np
import scipy.optimize as opt

from deap import (
    algorithms,
    base,
    creator,
    tools
    )

from . import util_funcs
from . import Full_Model_stress

from pathlib import Path

#Numpy presets
np.seterr(all='raise') #tell numpy to raise floating point errors.

# Create output folder if it doesn't exist
output_dir = Path.home() / 'Desktop' / 'SMA_REACT_output'
output_dir.mkdir(parents=True, exist_ok=True)

def cxTwoPointCopy(ind1, ind2):
    """Execute a two points crossover with copy on the input individuals. The
    copy is required because the slicing in numpy returns a view of the data,
    which leads to a self overwritting in the swap operation. It prevents:
    ::

        >>> import numpy
        >>> a = numpy.array((1,2,3,4))
        >>> b = numpy.array((5.6.7.8))
        >>> a[1:3], b[1:3] = b[1:3], a[1:3]
        >>> print(a)
        [1 6 7 4]
        >>> print(b)
        [5 6 7 8]

    Parameters
    ----------
    ind1 : LIST
        vector that defines individual one
    ind2 : LIST
        vector that defines individual two

    Returns
    -------
    ind1 : LIST
        New individual with crossover applied
    ind2 : LIST
        New individual with crossover applied
    """
    size = len(ind1)
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = (
        ind2[cxpoint1:cxpoint2],
        ind1[cxpoint1:cxpoint2],
    )
    return ind1, ind2

def psh(popSize, genSize, toolbox):
    """Generates DEAP things.

    Parameters
    ----------
    popSize : int
        Population size for GA
    genSize : int
        Number of generations for GA
    toolbox : deap
        DEAP toolbox.

    Returns
    -------
    pop : [type]
        Population
    stats : [type]
        Statistics
    hof : [type]
        Hall of Fame
    """
    # random.seed(64)
    pop = toolbox.population(n=popSize)
    # Numpy equality function (operators.eq) between two arrays returns the
    # equality element wise, which raises an exception in the if similar()
    # check of the hall of fame. Using a different equality function like
    # numpy.array_equal or numpy.allclose solve this issue.
    hof = tools.HallOfFame(1, similar=np.array_equal)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    algorithms.eaSimple(
        pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=genSize, stats=stats, halloffame=hof
    )
    print(hof)
    return pop, stats, hof

def exponentialBounds(value, bounds=[1e3, 1e8]):
    """Creates a bounded function based on an exponential distribution.
    Very convenient for values that span many orders of magnitude
    (i.e., the rise time k).

    Parameters
    ----------
    value : flt
        Entry in the design vector
    bounds : list, optional
        bounds for the specific entry in the design vector.
        By default [1e3, 1e8].

    Returns
    -------
    boundedValue : flt
        Un-normalized value for the entry in the design vector.
    """
    a = bounds[0]  # lower bound
    b = bounds[1] / a  # upper bound
    boundedValue = a * b ** (value / 1.0)  # tau (time constant) is one
    return boundedValue



def resizeBounds(value, bounds=[1e3, 1e8]):
    """Maps an entry of the design vector (bounds [0,1]) to the isotropic
    hardening modulus.

    Parameters
    ----------
    value : flt
        Entry in the design vector
    bounds : list, optional
        bounds for the specific entry in the design vector.
        By default [1e3, 1e8].

    Returns
    -------
    value : flt
        Bounded entry in the design vector.
    """
    value = (bounds[1] - bounds[0]) * value + bounds[0]
    return value

def evaluate(
        x,
        data,
        calWin,
        GA_data = False,
        plot_flag = False,
        gradient_flag=False,
        final_flag=False
        ):
    '''
    Evaluates the current design vector, measures the error between
    the model prediction and experimental data, re-plots the
    GUI outputs (strain-temperature history, design vector, etc.),
    and returns the error to the optimizer.

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    data : dict
        dictionary to contain problem-specific data,
        including (but not limited to) variable bounds and flags and
        experimental stress-strain-temperature histories.
    calWin : class
        class that describes the calibration progress window
        (animated plots).
    GA_data : list of lists, optional
        data passed from the genetic algorithm
        for aggregate stats. the two fields are the
        minimum objective value and the average objective
        value for each generation.
        The default is False.
    plot_flag : bool, optional
        flag to update plots. The default is False.
    gradient_flag : bool, optional
        flag to specify whether the optimization
        is a genetic algorithm or gradient-based.
        The only thing it changes here is the frequency
        of plotting.
        The default is False.
    final_flag : bool, optional
        flag to specify the last (optimal) functional evaluation.
        plots the best result in the calibration progress window.
        The default is False.

    Returns
    -------
    flt
        error of the evaluation.

    '''
    # INPUT: stress/strain/temperature, material properties (P)

    bounds = data['bounds']
    boundedX = np.zeros(shape=len(x))
    prop_count = 0
    for j in range(len(x)):
        boundedX[j] = resizeBounds(x[j], bounds=list(bounds[j]))


    P = data['P']

    DV_order = ['E_M','E_A', 'M_s', 'M_f', 'A_s', 'A_f', 'C_M', 'C_A', 'H_min',
            'H_max - H_min', 'k', 'n_1', 'n_2', 'n_3', 'n_4', 'sig_crit', 'alpha']

    prop_count = 0
    DV_count = 0
    for DV in DV_order:
        if data['DV_flags'][prop_count] == True:
            #if DV == 'E_A':
            #    P['E_A'] = P['E_M'] - boundedX[DV_count]
            if DV == 'M_f':
                P['M_f'] = P['M_s'] - boundedX[DV_count]
            elif DV == 'A_f':
                P['A_f'] = P['A_s'] + boundedX[DV_count]
            elif DV == 'H_max - H_min':
                P['H_sat'] = P['H_min'] + boundedX[DV_count]
            else:
                P[DV] = boundedX[DV_count]
            DV_count +=1
        else:
            pass
        prop_count +=1

    if data['modulus_flag'] == True: #Set E_A = E_M
        P['E_A'] = P['E_M']

    if data['slope_flag'] == True: #Set C_A = C_M
        P['C_A'] = P['C_M']

    if data['smooth_hardening_flag'] == True: #Set n_1 = n_2 = n_3 = n_4
        P['n_2'] = P['n_1']
        P['n_3'] = P['n_1']
        P['n_4'] = P['n_1']

    #P['sig_crit'] = 0.

    # Coefficient of thermal expansion
    #P['alpha'] = 0.

    #Optimizer properties
    # This commented dictionary is an optimal solution
    # P = {
    #     "H_min": 0.0,
    #     "n_1": 0.87653784841218,
    #     "sig_crit": 0.0,
    #     "E_M": 20240000000.0,
    #     "E_A": 59140000000.0,
    #     "M_s": 400,
    #     "M_f": 360,
    #     "A_s": 440,
    #     "A_f": 490,
    #     "C_M": 7000000.0,
    #     "C_A": 5000000.0,
    #     "H_sat": 0.01653878349352556,
    #     "k": 1.14e-08,
    #     "alpha": 1.07e-06,
    #     "n_2": 0.4121679791587434,
    #     "n_3": 0.5054753785815483,
    #     "n_4": 0.28761867011171693,
    #     "delta": 1e-06,
    #     "sig_cal": 100000000.0,
    #     "MVF_tolerance": 0.0001,
    #     "H_sat": 0.0165
    # }


    # Algorithmic delta for modified smooth hardening function
    P['delta']=data['delta']

    # Calibration Stress
    P['sig_cal']=data['sigma_cal']

    # Tolerance for change in MVF during implicit iteration
    P['MVF_tolerance']=data['MVF_tol']

    # P['E_A'] = 54.514E9
    # P['E_M'] = 17.39E9
    # P['M_s'] = 180 + 273.15
    # P['M_f'] = P['M_s'] - 5.0
    # P['A_s'] = 208 + 273.15
    # P['A_f'] = P['A_s'] + 5.0
    # P['C_A'] = 16.54E6
    # P['C_M'] = 16.25E6
    # P['H_min'] = 0.0
    # P['H_sat'] = 0.01696
    # P['k'] = 0.01261E-6
    # P['sig_crit'] = 0.0
    # P['alpha'] = 8.82E-6
    # P['n_1'] = 1.0
    # P['n_2'] = 1.0
    # P['n_3'] = 1.0
    # P['n_4'] = 1.0



    i = 0
    eps_model_total = []
    T_total = []
    num_experiments = data['num_experiments']
    errors = np.zeros(shape=num_experiments)
    for i in range(num_experiments):
        eps = data['exp_'+str(i)]['strain']
        T = data['exp_'+str(i)]['temperature']
        sigma = data['exp_'+str(i)]['stress']



        #Solver options
        elastic_check = 'N'
        integration_scheme = 'I'

        error_flag = 'two_norm'
        try:
            eps_model= Full_Model_stress.Full_Model_stress(
                T,
                sigma,
                P,
                elastic_check,
                integration_scheme
                )[0]
            eps_model_total.append(eps_model)
            T_total.append(T)
            if error_flag == 'two_norm':
                errors[i] = util_funcs.minkowski_error(
                    eps,
                    eps_model,
                    order=2
                    )
            elif error_flag == 'infinity_norm':
                errors[i] = util_funcs.minkowski_error(
                    eps,
                    eps_model,
                    order=10
                    )
            elif error_flag == 'hausdorff':
                errors[i] = util_funcs.symmetric_hausdorff(
                    eps.to_numpy()[..., np.newaxis],
                    eps_model[..., np.newaxis]
                    )
        except:
            errors[i] = 1E12
        i +=1


    if plot_flag == True:
        try:
            for i in range(len(eps_model_total)):
                file_name = 'optimal_model_'+str(i)+'.csv'
                output_dir = Path.home() / 'Desktop' / 'SMA_REACT_output'
                output_file = os.path.join(output_dir,file_name)
                model_prediction = np.zeros(shape=(len(eps_model_total[0]),2))
                model_prediction[:,0] = np.array(T_total[i])
                model_prediction[:,1] = eps_model_total[i]
                np.savetxt(output_file,model_prediction,delimiter=',')

            # plot_strain_temperature(T_total,eps_model_total,i,d)
            calWin.update_temp_strain(T_total, eps_model_total, len(eps_model_total))
            calWin.update_phase_diagram(P, [0, 200E6])
            calWin.update_design_variable_vals(x,data['DV_flags'])
        except:
            pass

    if gradient_flag == True:
        calWin.gens = GA_data[0]
        calWin.mins = GA_data[1]
        calWin.gens.append(max(calWin.gens)+1)
        if np.mean(errors) < calWin.mins[-1]:
            calWin.mins.append(np.mean(errors))
        else:
            calWin.mins.append(calWin.mins[-1])
        calWin.update_opt_progress(calWin.gens, calWin.mins,calWin.mins, 0.0)

    if final_flag == True:
        # pprint(x)
        pprint.pprint(P)

    if error_flag in ['two_norm','infinity_norm']:
        return np.mean(errors),
    if error_flag == 'hausdorff':
        return np.max(errors),



def optimizer(toolbox,popSize,genSize,data, calWin, seed=None):
    '''
    Runs the hybrid optimization to find optimal
    material properties.
    
    Parameters
    ----------
    toolbox : class
        deap-specific class that contains evolutionary operators.
        for more information, see:
            https://deap.readthedocs.io/en/master/api/base.html#toolbox
    popSize : int
        population size for each generation.
    genSize : int
        number of generations.
    data : dict
        dictionary that contains number of experiments, experimental data, etc.
    calWin : class
        pyqt class that defines the calibration progress window
        (animated plots).
    seed : int, optional
        seed for random reproducibility. The default is None.

    Returns
    -------
    pop : list of lists
        the current population of design variables
    logbook : class
        deap-specific class that contains ``Evolution records
        as a chronological list of dictionaries.'' for more information, see:
        https://deap.readthedocs.io/en/master/api/tools.html?highlight=logbook#logbook
    d : class
        class to dynamically update matplotlib plots.

    '''
    random.seed(seed)

    CXPB = 0.9 #crossover probability
    nGenSave = 20 #Best population will be saved every nGenSave
    i = 0
    d = util_funcs.DynamicUpdate()

    #collect the data into one dictionary
    num_experiments = data['num_experiments']
    for i in range(num_experiments):
        eps,T = data['exp_'+str(i)]['strain'],data['exp_'+str(i)]['temperature']
        #T =


        if i == 0:
            total_strain = eps
            total_temperature = T
        else:
            total_strain = np.concatenate((total_strain,eps))
            total_temperature = np.concatenate((total_temperature,T))

        i +=1

    # d.on_launch(total_temperature,total_strain,i)
    calWin.plot_experimental(total_temperature, total_strain, i)



    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    pop = toolbox.population(n=popSize)

    # Evaluate the individuals with an invalid fitness (ind. that need to be updated)
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    #HERE WE CAN ELIMINATE SERIAL MAPPING AND REPLACE WITH BATCH CALCULATION
    #WE IGNORE THE 'EVALUATE' DEVICE COMPLETELY, SINCE IT IS FOR A SINGLE DESIGN
    # fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    arrayofGenes = []
    gen=0
    for ind in invalid_ind:
        arrayofGenes.append(ind)
        ind.fitness.values = evaluate(ind,data, calWin)

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))

    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    totGen = 1
    gen = 1
    cntGenSave = 1

    while gen < genSize+1:
        # Vary the population
        offspring = toolbox.select(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        arrayofGenes = []
        for ind in invalid_ind:
            arrayofGenes.append(ind)
            ind.fitness.values = evaluate(ind,data, calWin)

        # Select the next generation population
        pop = toolbox.select(pop + offspring, popSize)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)
        #pop.sort(key=lambda x: x.fitness.values)
        log_dir = Path.home() / 'Desktop' / 'SMA_REACT_output'
        log_dir.mkdir(parents=True, exist_ok=True)
        shelve_path = str(log_dir / 'popLog')  # Must be str for shelve
        db=shelve.open(shelve_path)
        db['lastPop']=pop
        if cntGenSave == nGenSave:
            db[repr(gen)+'Pop']=pop
            cntGenSave = 0
        db.close()


        # Write a color map illustrating the genes of all the best population members
        # throughout the generations
        calWin.gens = logbook.select('gen')
        calWin.mins = logbook.select('min')

        avg = logbook.select('avg')
        std = logbook.select('std')
        calWin.update_opt_progress(
            calWin.gens,
            calWin.mins,
            avg,
            std
            )
        #print(pop[0])
        calWin.update_design_variable_vals(
            pop[0],
            data['DV_flags']
            )


        #pop[0] is the best current individual
        error = evaluate(pop[0],data,calWin,GA_data=False,
                         plot_flag=True,
                         gradient_flag = False,final_flag=False)
        cntGenSave +=1
        gen += 1
        totGen += 1

    return pop, logbook,d



#if __name__ == '__main__':
def main(bounds,calibration_class,data,calWin):
    '''
    Initialize and run the optimization.

    Parameters
    ----------
    bounds : list of lists
        bounds for each active design variable.
        the structure is [[lower_bound_1, upper_bound_1], [...], ...]
    calibration_class : class
        calibration parameters widget, contains all flags and values.
    data : dict
        dictionary containing experimental data/calibration specifics/etc.
    calWin : class
        calibration progress widget, dynamically updates plots.

    Returns
    -------
    error : float
        final error for the optimization.

    '''
    util_funcs.plot_settings(format_flag="presentation")

    #set both moduli (E_M and E_A) equal to each other
    data['modulus_flag'] = calibration_class.flags['modulus_flag']
    #set both stress-influence coefficients (C_M and C_A) equal to each other
    data['slope_flag'] = calibration_class.flags['slope_flag']
    #flag to set all smooth hardening coefficients (n_1 -- n_4) equal
    data['smooth_hardening_flag'] = calibration_class.flags['smooth_hardening_flag']
    data['DV_flags'] = calibration_class.DV_flags
    known_values = calibration_class.known_values


    #If we want both moduli to be the same, just make the E_M - E_A DV inactive
    if data['modulus_flag'] == True:
        data['DV_flags'][1] = False

    data['delta'] = calibration_class.delta.value
    data['sigma_cal'] = calibration_class.sigma_cal.value
    data['MVF_tol'] = calibration_class.MVF_tol.value


    num_DVs = data['DV_flags'].sum()

    ## Initialize bounds based on the DV_flags
    data['bounds'] = bounds
    data['P'] = known_values

    # Population size for GA (must be divisible by 4)
    popSize = int(calibration_class.pop_size)
    # Number of generations for GA
    genSize = int(calibration_class.num_gens)
    # Maximum iterations for the gradient-based optimizer
    maxIterGradient = int(calibration_class.num_iters)

    # DEAP
    creator.create(
        "FitnessMin", base.Fitness, weights=(-1.0,)
    )  # Create a single-objective minimization
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.random)
    toolbox.register(
        "individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=num_DVs
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register(
        "evaluate",
        evaluate,
        data = data
    )
    toolbox.register("mate", cxTwoPointCopy)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    # startTime = time.perf_counter()
    pop, stats = optimizer(toolbox,popSize,genSize,data, calWin)[0:2]

    print('\n')
    print('Entering gradient-based optimizer')
    print('\n')
    generations = stats.select('gen')
    min_func_val = stats.select('min')
    GA_data = [generations,min_func_val]
    bounds = opt.Bounds(0,1)
    res2 = opt.minimize(
        evaluate,
        pop[0],
        method="SLSQP",
        options={"maxiter": maxIterGradient,
                  "disp":True},
        bounds = bounds,
        args=(
            data, calWin,GA_data,True,True
        ),
        #callback=calWin.updateDVVals,
    )

    error = evaluate(res2.x,data, calWin,
                     GA_data = False,
                     plot_flag=True,
                     gradient_flag=False,
                     final_flag=True)

    return error
