# # IMPORT STATEMENTS
# import pandas as pd
# from data_reader import reader
# from find_cycles import find_cycles
# from functions import export_all
# from moving_average_filter import movavg_filter
# from plot_temp_vs_strain import plot_temp_vs_strain
# from plot_3d import plotSST
# from low_pass_filter import lowpassFilter
# from high_pass_filter import highpassFilter
#
#
# def analyze_fmts(fluke, fluke_temp_title, interval, startTime, mts_filename, glitch_check, temp_title, disp_title, shape, unit_out, area, movavg_conditions, datapoints_dict, orig_length, bandpass, delay, end, no_cycles):
#     # EXTRACTING FLUKE DATA
#     # fluke = reader("Fluke Jacob 3 cycles.csv")
#     # fluke.extract()
#     # pd.options.mode.chained_assignment = None
#     fluke_data = fluke.dataframe[["Duration", fluke_temp_title]]
#     # if delay > 0:
#     #     durations = fluke_data["Duration"].to_list()
#     #     durations = [x + delay for x in durations]
#     #     fluke_data["Duration"] = durations
#
#
#
#
#     # CONVERTING THE DURATIONS TO TIME ELAPSED SINCE START AND FORMATTING THEM
#     # fluke_data = fluke_data.head(-1)
#     # durations = fluke_data["Duration"].tolist()
#     # for z in range(len(durations)):
#     #     if type(durations[z]) == str:
#     #         if durations[z].count(":") == 2:
#     #             durations[z] = datetime.datetime.strptime(durations[z], "%H:%M:%S.%f")
#     #         elif durations[z].count(":") == 1:
#     #             durations[z] = datetime.datetime.strptime(durations[z], "%M:%S.%f")
#     # for i in range(len(durations)):
#     #     durations[i] = datetime.timedelta(hours=durations[i].hour, minutes=durations[i].minute,
#     #                                       seconds=durations[i].second,
#     #                                       microseconds=durations[i].microsecond)
#     #     durations[i] = durations[i].total_seconds()
#     # for j in range(1, len(durations)):
#     #     durations[j] = durations[j] + durations[j - 1]
#     # for k in range(len(durations)):
#     #     durations[k] = round(durations[k], 3)
#     # fluke_data["Duration"] = durations
#
#
#     # RENAMING THE DURATIONS COLUMN TO TIME ELAPSED
#     fluke_data = fluke_data.rename(columns={"Duration": "Time Elapsed (s)"})
#
#
#     # EXTRACTING THE START TIME
#     start_time = fluke.start_time
#
#
#     # CONVERTING ALL THE DATA TO FLOATS
#     for column_label in range(1, len(fluke_data.columns)):
#         fluke_data[fluke_data.columns.tolist()[column_label]] = [float(x) for x in fluke_data[
#             fluke_data.columns.tolist()[column_label]].tolist()]
#
#
#     # PIVOTING FLUKE DATA
#     # end = float(input("Enter end time in seconds(s) "))
#     # end = fluke_data["Time Elapsed (s)"].tolist()[len(fluke_data["Time Elapsed (s)"]) - 1]
#     #interval = float(input("Enter time interval in seconds(s) "))
#     fluke_data = fluke_data.groupby(pd.cut(fluke_data["Time Elapsed (s)"], pd.interval_range(start=startTime, end=end, freq=interval, closed="left"))).mean()
#     del fluke_data["Time Elapsed (s)"]
#
#
#     # EXTRACTING MTS DATA
#     mts = reader(mts_filename)
#     mts.extract()
#     mts_data = mts.dataframe.copy()
#
#     if delay != 0:
#         time_key = mts_data.columns.tolist()[0]
#         durations = mts_data[time_key]
#         durations = [x - abs(delay) for x in durations]
#         mts_data[time_key] = durations
#
#
#     # INITIALIZING MTS TEMPERATURE TITLE VARIABLE
#     # temp_title_unformat, column_list = header_choice(mts_data.columns.tolist(), "MTS temperature")
#     # temp_title = mts_data.columns[column_list.index(temp_title_unformat.lower().replace(" ", ""))]
#
#
#     # ACCOUNTING FOR GLITCH IN THE MTS
#     # print("Sometimes the MTS glitches at 0 degrees.")
#     # glitch_check = input("Would you like to account for this glitch in the MTS and delete all spurious zeroes (Yes/No)? ")
#     if glitch_check.lower() == "yes":
#         for k in range(20):
#             delete_list = []
#             j=1
#             for i in range(1, len(mts_data[temp_title])):
#                 if mts_data[temp_title].iloc[i] == 0 and mts_data[temp_title].iloc[i+1] < 0.5:
#                     delete_list.append(i)
#                     j += 1
#             mts_data = mts_data.drop(mts_data.index[delete_list])
#
#
#     # PIVOTING MTS DATA
#     time_label = [y for y in mts_data.columns.tolist() if y.lower().find("time") >= 0]
#     mts_data = mts_data.groupby(pd.cut(mts_data[time_label[0]], pd.interval_range(start=startTime, end=end, freq=interval, closed="left"))).mean()
#     del mts_data[time_label[0]]
#
#
#     # COMBINING THE MTS AND FLUKE DATA
#     combined_data = pd.concat([fluke_data, mts_data], axis=1)
#
#
#     # INTERPOLATING THE DATA
#     for data_label in combined_data.columns:
#         combined_data[data_label] = combined_data[data_label].interpolate(method="linear", limit_direction="forward")
#
#
#     # FINDING THE DISPLACEMENT
#     # column_headers = combined_data.columns.tolist()
#     # disp_title_unformat, new_headers = header_choice(column_headers, "displacement")
#     displacement = combined_data[disp_title]
#     disp_units = disp_title[-4:].strip()
#     # disp_title = combined_data.columns[new_headers.index(disp_title_unformat.lower())]
#
#
#     # MOVING AVERAGE FILTER
#     List_of_loads, mov_avg_set, unit, figure1, figure2 = movavg_filter(combined_data, temp_title, disp_title, movavg_conditions, datapoints_dict,
#                                                              fluke_check=True, fluke_temp_title=fluke_temp_title)
#
#
#     # INTERPOLATING THE MOVING AVERAGES
#     # for column in combined_data.columns:
#     #     if "Moving Average" in column:
#     #         combined_data[column] = combined_data[column].interpolate(method="linear", limit_direction="backward")
#
#
#     # CALCULATING STRESS AND ADDING IT TO DATAFRAME
#     # area, unit_out, shape = Geometry_input()
#     Stresses = []
#     if "load" in mov_avg_set:
#         search = ""
#         for col in combined_data.columns:
#             if "Load Moving Average" in col:
#                 search = col
#         for force in combined_data[search]:
#             stress = force/area
#             Stresses.append(stress)
#     else:
#         for force in List_of_loads:
#             stress = force / area
#             Stresses.append(stress)
#
#     stress_col_name = 'Stress' + ' (' + unit + '/' + unit_out + '^2)'
#     combined_data[stress_col_name] = Stresses
#
#
#     # CALCULATING THE STRAIN FROM THE DISPLACEMENT AND LENGTH
#     length = orig_length
#     strains = []
#     if "extension" in mov_avg_set or "all" in mov_avg_set:
#         for disp in combined_data["Displacement Moving Average"].tolist():
#             strains.append(disp/length)
#     else:
#         for disp in displacement:
#             strains.append(disp / length)
#     combined_data["Strain"] = strains
#
#
#     # BANDPASS FILTERING
#     choice = bandpass["Choice"]
#     if choice:
#         if bandpass["Type"] == "low":
#             combined_data["Filtered Strain"] = lowpassFilter(bandpass["Order"], bandpass["Sample Rate"], bandpass["Cutoff Frequency"], combined_data["Strain"])
#         elif bandpass["Type"] == "high":
#             combined_data["Filtered Strain"] = highpassFilter(bandpass["Order"], bandpass["Sample Rate"], bandpass["Cutoff Frequency"], combined_data["Strain"])
#
#
#     # RENAMING COLUMNS WTH UNITS
#     # for label in combined_data.columns:
#     #     if label.lower().find("sample") >= 0:
#     #         combined_data = combined_data.rename(columns={label: "Sample (°C)"})
#
#
#     # ADDING CYCLE NUMBERS TO THE DATAFRAME
#     find_cycles(combined_data, temp_title)
#
#
#     # EXPORTING DATA
#     export_all(combined_data, start_time, shape, area, unit_out, length, disp_units, "MTS + Fluke.xlsx")
#
#
#     # PLOTTING DATA
#     if "temperature" in mov_avg_set or "all" in mov_avg_set:
#         temp_strain_plot = plot_temp_vs_strain(combined_data, "MTS Temperature Moving Average", choice, no_cycles, fluke_check=True, fluke_temp_title="Fluke Temperature Moving Average")
#         figure3d = plotSST(combined_data, "MTS Temperature Moving Average", stress_col_name, fluke_check=True)
#     else:
#         temp_strain_plot = plot_temp_vs_strain(combined_data, temp_title, choice, no_cycles, fluke_check=True, fluke_temp_title=combined_data.columns.tolist()[1])
#         figure3d = plotSST(combined_data, temp_title, stress_col_name, fluke_check=True)
#
#     # EXPORTING FOR ASMADA
#     asm_cols = [temp_title, fluke_temp_title, stress_col_name, "Strain"]
#     if "temperature" in mov_avg_set or "all" in mov_avg_set:
#         asm_cols.insert(2, "MTS Temperature Moving Average")
#         asm_cols.insert(3, "Fluke Temperature Moving Average")
#     asmada_df = combined_data[asm_cols]
#     asmada_df.to_csv("ASMADA Data.csv", index=False)
#
#
#     return figure1, figure2, temp_strain_plot, figure3d

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
    asmada_df.to_csv("output/clean_data_TSE.csv", index=False)

    # PLOTTING DATA
    start_index = final_df["Relative Time"].searchsorted(relative_start_time, side="left")
    end_index = final_df["Relative Time"].searchsorted(relative_end_time, side="right")
    df_to_plot = final_df.iloc[start_index:end_index + 1, :]
    df_to_plot.to_csv("output/processed_synced.csv")
    if "temperature" in mov_avg_set or "all" in mov_avg_set:
        temp_vs_strain_plot, colorbar_error = plot_temp_vs_strain(df_to_plot, "MTS Temperature Moving Average", choice, no_cycles, True,
                                                  "Fluke Temperature Moving Average")
        temp_vs_stress_vs_strain_plot = plotSST(df_to_plot, "MTS Temperature Moving Average", stress_title, choice,
                                                no_cycles, True, "Fluke Temperature Moving Average")
    else:
        temp_vs_strain_plot, colorbar_error = plot_temp_vs_strain(df_to_plot, mts_temp_title, choice, no_cycles, True, fluke_temp_title)
        temp_vs_stress_vs_strain_plot = plotSST(df_to_plot, mts_temp_title, stress_title, choice, no_cycles,
                                                True, fluke_temp_title)

    # EXPORTING DATA
    #final_df.to_csv("output/MTS + Fluke.csv", index=True)

    # RETURNING PLOTS
    plots = [temp_vs_strain_plot, temp_vs_stress_vs_strain_plot]
    if len(mov_avg_set) != 0 and "none" not in mov_avg_set:
        plots.extend([mts_mov_avg_fig, fluke_mov_avg_fig])
    return plots, colorbar_error, cycle_error
