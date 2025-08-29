
# IMPORT STATEMENTS

import datetime
import pandas as pd
import numpy as np
from src.preprocessor.data_reader import reader
from src.preprocessor.find_cycles import find_cycles
from src.preprocessor.plot_temp_vs_strain import plot_temp_vs_strain
from src.preprocessor.moving_average_filter import movavg_filter
from src.preprocessor.plot_3d import plotSST
from src.preprocessor.low_pass_filter import lowpassFilter
from src.preprocessor.high_pass_filter import highpassFilter
from pathlib import Path
from collections import Counter

# parameters
# disp_title = "Extension (mm)"
# mts_temp_title = "_COM1 (C)"
# fluke_temp_title = "Sample"
# area = 40
# area_unit = "mm"
# orig_length = 10
# mov_avg_set = {"all"}
# datapoints = {"MTS Temperature": 30, "Fluke Temperature": 30, "Load": 30, "Displacement": 30}
# bandpass = {"Choice": False}
# mts_start_time = "1/23/2019 9:27:54"
# no_cycles = False
# glitch_check = "yes"
# cycle_determiner = "fluke"
# relative_start_time = 10145.8
# relative_end_time = 15780.7

def analyze_fmts(mts_temp_title, fluke_temp_title, disp_title, area, area_unit, orig_length, mov_avg_set, datapoints,
                 bandpass, mts_start_time, no_cycles, glitch_check, cycle_determiner, relative_start_time,
                 relative_end_time, mts_file_name, fluke_file_name):
    # EXTRACTING FLUKE DATA
    fluke_data = reader(fluke_file_name)
    fluke_data.extract_fluke()
    fluke_start_day = fluke_data.start_time.split()[0]
    fluke = fluke_data.dataframe
    if ("/" in fluke["Start Time"].iloc[0]):
        fluke["Start Time"] = [datetime.datetime.strptime(x, "%m/%d/%Y %H:%M:%S.%f") for x in fluke["Start Time"]]
    else:
        fluke["Start Time"] = [datetime.datetime.strptime("{} {}".format(fluke_start_day, x), "%m/%d/%Y %H:%M:%S.%f")
                               for x in fluke["Start Time"]]
    str_cols = []
    for col in fluke.columns:
        try:
            fluke[col] = fluke[col].astype(float)
        except:
            if col != "Start Time":
                str_cols.append(col)

    # EXTRACTING MTS DATA
    mts_data = reader(mts_file_name)
    mts_data.extract_txt()
    mts = mts_data.dataframe
    time_col = mts.iloc[:, 0]
    mts_start = datetime.datetime.strptime("{} {}".format(fluke_start_day, mts_start_time), "%m/%d/%Y %H:%M:%S")
    abs_times = [mts_start + datetime.timedelta(seconds=time) for time in time_col]
    mts.insert(0, "Global Time", abs_times)

    # ACCOUNTING FOR GLITCH IN THE MTS
    if glitch_check.lower() == "yes" and len(set(mts[mts_temp_title])) > 1:
        for k in range(20):
            delete_list = []
            j = 1
            for i in range(1, len(mts[mts_temp_title])):
                if mts[mts_temp_title].iloc[i] == 0 and mts[mts_temp_title].iloc[i + 1] < 0.5:
                    delete_list.append(i)
                    j += 1
            mts = mts.drop(mts.index[delete_list])

    # FINDING MIN TIME SEPARATION FOR RESAMPLING
    # min interval for mts
    mts_diffs = [str(x)[str(x).index(".") + 1:] for x in np.diff(np.array(abs_times))]
    for i in range(len(mts_diffs)):
        idx = len(mts_diffs[i]) - 1
        while mts_diffs[i][idx] == "0":
            idx -= 1
        mts_diffs[i] = len(mts_diffs[i][:idx + 1])
    occurrences = Counter(mts_diffs)
    num_digit_sep = 0
    for k in range(max(mts_diffs), -1, -1):
        if occurrences[k]/len(mts_diffs) * 100 > 4.6:
            num_digit_sep = k
            break
    min_time_sep = 1/(10**num_digit_sep)

    # RESAMPLING THE MTS AND FLUKE DATA
    sep = "{}S".format(min_time_sep)
    mts = mts.set_index("Global Time").resample(sep).interpolate()
    for i in range(len(mts.columns)):
        if type(mts.iloc[0, i]) == str:
            mts[mts.columns[i]] = mts[mts.columns[i]].interpolate(method='pad')
    fluke = fluke.set_index("Start Time").resample(sep).interpolate()
    for col in str_cols:
        fluke[col] = fluke[col].interpolate(method="pad")
    final_df = pd.concat([fluke, mts], axis=1).dropna()

    # ADDING A RELATIVE TIME COLUMN
    relative_time = [x * min_time_sep for x in range(len(final_df.index))]
    final_df.insert(0, "Relative Time", relative_time)

    # FINDING LOAD COLUMN
    load_col_name = [x for x in final_df.columns if "load" in x.lower()][0]
    load_col_unit = load_col_name[load_col_name.index('(') + 1: load_col_name.index(")")]

    # MOVING AVERAGE FILTERING
    if len(mov_avg_set) != 0 and "none" not in mov_avg_set:
        mts_mov_avg_fig, fluke_mov_avg_fig = movavg_filter(final_df, mts_temp_title, disp_title, load_col_name,
                                                           mov_avg_set, datapoints, True, fluke_temp_title)

    # CALCULATING STRESS
    if "load" in mov_avg_set or "all" in mov_avg_set:
        stress = [load/area for load in final_df["Load Moving Average"]]
    else:
        stress = [load/area for load in final_df[load_col_name]]
    stress_title = "Stress ({}/{}^2)".format(load_col_unit, area_unit)
    final_df[stress_title] = stress

    # CALCULATING STRAIN
    if "displacement" in mov_avg_set or "all" in mov_avg_set:
        strain = [disp/orig_length for disp in final_df["Displacement Moving Average"]]
    else:
        strain = [disp/orig_length for disp in final_df[disp_title]]
    final_df["Strain"] = strain

    # BANDPASS FILTERING
    # choice = bandpass["Choice"]
    choice = False
    if choice:
        if bandpass["Type"] == "low":
            final_df["Filtered Strain"] = lowpassFilter(bandpass["Order"], bandpass["Sample Rate"],
                                                             bandpass["Cutoff Frequency"], final_df["Strain"])
        elif bandpass["Type"] == "high":
            final_df["Filtered Strain"] = highpassFilter(bandpass["Order"], bandpass["Sample Rate"],
                                                              bandpass["Cutoff Frequency"], final_df["Strain"])

    # ADDING CYCLE NUMBERS TO THE DATAFRAME
    if cycle_determiner.lower() == "fluke":
        cycle_error = find_cycles(final_df, fluke_temp_title)
    elif cycle_determiner.lower() == "mts":
        cycle_error = find_cycles(final_df, mts_temp_title)
    if cycle_error:
        no_cycles = True

    # # EXPORTING FOR ASMADA
    asm_cols = [stress_title, "Strain"]
    if "temperature" in mov_avg_set or "all" in mov_avg_set:
        asm_cols.insert(0, "MTS Temperature Moving Average")
        asm_cols.insert(1, "Fluke Temperature Moving Average")
    else:
        asm_cols.insert(0, mts_temp_title)
        asm_cols.insert(1, fluke_temp_title)
    if choice:
        asm_cols.append("Filtered Strain")
    asmada_df = final_df[asm_cols]
    asmada_df = final_df[asm_cols].replace("", pd.NA).dropna().reset_index(drop=True) #remove empty space from moving average filter
    
    script_dir = Path(__file__).resolve().parent  
    output_dir = script_dir.parent.parent / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure the output directory exists
    file_path = output_dir / "clean_data_TSE.csv"
    asmada_df.to_csv(file_path)
    
    #asmada_df.to_csv("output/clean_data_TSE.csv", index=False)

    # PLOTTING DATA
    start_index = final_df["Relative Time"].searchsorted(relative_start_time, side="left")
    end_index = final_df["Relative Time"].searchsorted(relative_end_time, side="right")
    df_to_plot = final_df.iloc[start_index:end_index + 1, :]
    file_path = output_dir / "processed_synced.csv"
    df_to_plot.to_csv(file_path)
    #df_to_plot.to_csv("output/processed_synced.csv")
    if "temperature" in mov_avg_set or "all" in mov_avg_set:
        temp_vs_strain_plot, colorbar_error = plot_temp_vs_strain(df_to_plot, "MTS Temperature Moving Average", choice, no_cycles, True,
                                                  "Fluke Temperature Moving Average")
        temp_vs_stress_vs_strain_plot = plotSST(df_to_plot, "MTS Temperature Moving Average", stress_title, choice,
                                                no_cycles, True, "Fluke Temperature Moving Average")
    else:
        temp_vs_strain_plot, colorbar_error = plot_temp_vs_strain(df_to_plot, mts_temp_title, choice, no_cycles, True, fluke_temp_title)
        temp_vs_stress_vs_strain_plot = plotSST(df_to_plot, mts_temp_title, stress_title, choice, no_cycles,
                                                True, fluke_temp_title)
    
    print(f"Output will be saved to: {output_dir}")
    # EXPORTING DATA
    #final_df.to_csv("output/MTS + Fluke.csv", index=True)

    # RETURNING PLOTS
    plots = [temp_vs_strain_plot, temp_vs_stress_vs_strain_plot]
    if len(mov_avg_set) != 0 and "none" not in mov_avg_set:
        plots.extend([mts_mov_avg_fig, fluke_mov_avg_fig])
    return plots, colorbar_error, cycle_error
