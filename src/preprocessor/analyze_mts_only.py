# IMPORT STATEMENTS
from collections import Counter
import numpy as np
import os
import sys

from src.preprocessor.functions import *
from src.preprocessor.data_reader import reader
from src.preprocessor.find_cycles import find_cycles
from src.preprocessor.moving_average_filter import movavg_filter
from src.preprocessor.plot_temp_vs_strain import plot_temp_vs_strain
from src.preprocessor.plot_3d import plotSST
from src.preprocessor.low_pass_filter import lowpassFilter
from src.preprocessor.high_pass_filter import highpassFilter
from pathlib import Path



def analyze_mts(file, end, start, glitch_check, temp_title, disp_title, shape, unit_out, area, movavg_conditions, datapoints_dict, orig_length, bandpass, no_cycles):
    # EXTRACTING MTS DATA
    mts = reader(file)
    mts.extract()
    mts_data = mts.dataframe
    time_col_name = mts_data.columns[0]
    if len(mts_data[time_col_name].tolist()) != len(set(mts_data[time_col_name].tolist())):
        mts_data = mts_data.groupby([time_col_name], as_index=False).mean()
    time_col = mts_data.iloc[:, 0]
    abs_times = [datetime.timedelta(seconds=time) for time in time_col]
    mts_data.insert(0, "Global Time", abs_times)


    # FINDING MIN TIME INTERVAL
    mts_diffs = [str(x.total_seconds())[str(x.total_seconds()).index(".") + 1:] for x in np.diff(np.array(abs_times))]
    for i in range(len(mts_diffs)):
        idx = len(mts_diffs[i]) - 1
        while mts_diffs[i][idx] == "0" and idx >= 0:
            idx -= 1
        mts_diffs[i] = len(mts_diffs[i][:idx + 1])
    occurrences = Counter(mts_diffs)
    num_digit_sep = 0
    for k in range(max(mts_diffs), -1, -1):
        if occurrences[k]/len(mts_diffs) * 100 > 4.6:
            num_digit_sep = k
    min_time_sep = 1 / (10 ** num_digit_sep)


    # ACCOUNTING FOR GLITCH IN THE MTS
    if glitch_check.lower() == "yes":
        for k in range(20):
            delete_list = []
            j=1
            for i in range(1, len(mts_data[temp_title])):
                if mts_data[temp_title].iloc[i] == 0 and mts_data[temp_title].iloc[i+1] < 0.5:
                    delete_list.append(i)
                    j += 1
            mts_data = mts_data.drop(mts_data.index[delete_list])


    # RESAMPLING DATA
    sep = "{}S".format(min_time_sep)
    mts_data = mts_data.set_index("Global Time").resample(sep).interpolate()

    # FINDING THE DISPLACEMENT
    displacement = mts_data[disp_title]
    # disp_units = disp_title[-4:].strip()


    # FINDING LOAD COLUMN
    load_col_name = [x for x in mts_data.columns if "load" in x.lower()][0]
    load_col_unit = load_col_name[load_col_name.index('(') + 1: load_col_name.index(")")]


    # MOVING AVERAGE FILTER
    if len(movavg_conditions) != 0 and "none" not in movavg_conditions:
        mov_avg_figure = movavg_filter(mts_data, temp_title, disp_title,
                                                     load_col_name, movavg_conditions, datapoints_dict)


    # CALCULATING STRESS AND ADDING IT TO MTS DATAFRAME
    if "load" in movavg_conditions or "all" in movavg_conditions:
        stress = [force/area for force in mts_data["Load Moving Average"]]
    else:
        stress = [force/area for force in mts_data[load_col_name]]

    stress_col_name = 'Stress' + ' (' + load_col_unit + '/' + unit_out + '^2)'
    mts_data[stress_col_name] = stress


    # CALCULATING THE STRAIN FROM THE DISPLACEMENT AND LENGTH
    if "displacement" in movavg_conditions or "all" in movavg_conditions:
        strains = [disp/orig_length for disp in mts_data["Displacement Moving Average"]]
    else:
        strains = [disp/orig_length for disp in displacement]
    mts_data["Strain"] = strains


    # BANDPASS FILTERING
    # choice = bandpass["Choice"]
    choice = False
    if choice:
        if bandpass["Type"] == "low":
            mts_data["Filtered Strain"] = lowpassFilter(bandpass["Order"], bandpass["Sample Rate"],
                                                        bandpass["Cutoff Frequency"], mts_data["Strain"])
        elif bandpass["Type"] == "high":
            mts_data["Filtered Strain"] = highpassFilter(bandpass["Order"], bandpass["Sample Rate"],
                                                         bandpass["Cutoff Frequency"], mts_data["Strain"])


    # ADDING CYCLE NUMBERS TO THE DATAFRAME
    cycle_error = find_cycles(mts_data, temp_title)
    if cycle_error:
        no_cycles = True


    # PLOTTING DATA
    start_index = mts_data.iloc[:, 0].searchsorted(start, side="left")
    end_index = mts_data.iloc[:, 0].searchsorted(end, side="right")
    df_to_plot = mts_data.iloc[start_index:end_index + 1, :]
    if "temperature" in movavg_conditions or "all" in movavg_conditions:
        final_plot, colorbar_error = plot_temp_vs_strain(df_to_plot, "MTS Temperature Moving Average", choice, no_cycles)
        figure3d = plotSST(df_to_plot, "MTS Temperature Moving Average", stress_col_name, choice, no_cycles)
    else:
        final_plot, colorbar_error = plot_temp_vs_strain(df_to_plot, temp_title, choice, no_cycles)
        figure3d = plotSST(df_to_plot, temp_title, stress_col_name, choice, no_cycles)


    # EXPORTING DATA
    # export_all(mts_data, start, shape, area, unit_out, orig_length, disp_units, "MTS_ONLY.xlsx")
    # Create output folder if it doesn't exist
    output_dir = Path.home() / 'Desktop' / 'SMA_REACT_output'
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure the output directory exists
    file_path = output_dir / "processed_MTS.csv"
    mts_data.to_csv(file_path)

    # EXPORTING FOR ASMADA
    asm_cols = [temp_title, stress_col_name, "Strain"]
    if "temperature" in movavg_conditions or "all" in movavg_conditions:
        asm_cols.insert(1, "MTS Temperature Moving Average")
    if choice:
        asm_cols.append("Filtered Strain")
    asmada_df = mts_data[asm_cols]
    asmada_df = mts_data[asm_cols].replace("", pd.NA).dropna().reset_index(drop=True) #remove empty space from moving average filter
    file_path = output_dir / "clean_data_TSE.csv"
    asmada_df.to_csv(file_path, index=False)

    plots = [final_plot, figure3d]
    if len(movavg_conditions) != 0 and "none" not in movavg_conditions:
        plots.append(mov_avg_figure)
    return plots, colorbar_error, cycle_error
