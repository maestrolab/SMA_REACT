# IMPORT STATEMENTS
import numpy as np
from scipy.signal import find_peaks


# function that determines what is considered a cycle and adds cycle numbers to the dataframe
#This might be ASMADA code? -Jacob 5/20/2025
def find_cycles(df, temp_title):
    # cycles error
    cycle_error = False

    try:
        # moving average to ensure accuracy of cycle detection
        temps = df[temp_title].rolling(window=int(0.00137 * len(df[temp_title]))).mean()

        min_peak_height = temps.mean(skipna=True)
        min_dist_btw_peaks = 50
        min_peak_prominence = round(temps.std(skipna=True))
        cycle_inds = find_peaks(temps, height=min_peak_height, distance=min_dist_btw_peaks, prominence=min_peak_prominence)
        cycle_inds = np.asarray(cycle_inds, dtype=object)[0]

        if cycle_inds.size == 0:
            cycle_inds = np.array([len(df.index) - 1])

        cycle_nums_to_append = np.empty([0,0], dtype=int)
        num_rows_in_file = len(df[temp_title])
        cur_cycle_num = 0

        for x in range(cycle_inds.size):
            if x == 0:
                cycle_nums_to_append = np.append(cycle_nums_to_append,
                                                    np.full((1, cycle_inds[x]),
                                                            cur_cycle_num,
                                                            dtype=int))

            cur_cycle_num += 1

            if x < cycle_inds.size - 1:
                cycle_nums_to_append = np.append(cycle_nums_to_append,
                                                    np.full((1, cycle_inds[x + 1] - cycle_inds[x]),
                                                            cur_cycle_num,
                                                            dtype=int))

            elif x == cycle_inds.size - 1:
                cycle_nums_to_append = np.append(cycle_nums_to_append,
                                                    np.full((1, num_rows_in_file - cycle_inds[x]),
                                                            cur_cycle_num,
                                                            dtype=int))
        df.insert(0, "Cycle", cycle_nums_to_append)
    except:
        cycle_error = True

    return cycle_error