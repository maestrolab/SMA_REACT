# IMPORT STATEMENTS
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

from src.preprocessor.data_reader import reader


def plotDSC(file_name, step_initial, step_final, x_axis, y_axis, filter, movavgx=0, movavgy=0):
    # extracting data from file
    dsc = reader(file_name)
    dsc.extract_DSC()
    data = dsc.dataframe

    # filtering data if necessary
    if filter:
        data["{} Moving Average".format(x_axis)] = data[x_axis].rolling(window=movavgx).mean()
        data["{} Moving Average".format(y_axis)] = data[y_axis].rolling(window=movavgy).mean()

    # extracting data from which steps the user wants
    step_list = []
    for i in range(step_initial, step_final + 1):
        step_list.append(i)
    step_data = data.loc[data["Step"].isin(step_list)]

    # getting values to plot
    if filter:
        temp_filtered = step_data["{} Moving Average".format(x_axis)]
        heat_flow_filtered = step_data["{} Moving Average".format(y_axis)]
    temps = step_data[x_axis]
    heat_flow = step_data[y_axis]

    # plotting
    dsc_fig = Figure()
    ax = dsc_fig.add_subplot(121)
    ax.plot(temps, heat_flow)
    ax.set_title("{} vs. {}".format(x_axis, y_axis))
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    if filter:
        ax2 = dsc_fig.add_subplot(122)
        ax2.plot(temp_filtered, heat_flow_filtered)
        ax2.set_title("Filtered Plot")
        ax2.set_xlabel(x_axis)
        ax2.set_ylabel(y_axis)

    # exporting to an excel file
    # writer = pd.ExcelWriter("DSC.xlsx")
    # data.to_excel(writer)
    # writer.save()
    # writer.close()
    
    with pd.ExcelWriter("output/DSC.xlsx", engine="openpyxl") as writer:
        data.to_excel(writer, index=False)

    return dsc_fig





