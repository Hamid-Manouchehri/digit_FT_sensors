#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyxdf
from os import getcwd
from os.path import join, abspath
import matplotlib.dates as mdates
from datetime import datetime


gelsight_mini_interface_dir = getcwd()  # WHATEVER/digit_FT_sensors/scripts
parent_dir = join(gelsight_mini_interface_dir, '..')  # Go one level up from the current_dir
parent_dir_abs = abspath(parent_dir)
dir_to_save_data = join(parent_dir_abs, 'data/')



def extract_seconds_from_timestamp(timestamp):
    '''
    Note: data sampling must take less than 60 min.
    '''
    time_in_seconds = timestamp.minute * 60 + timestamp.second + timestamp.microsecond / 1e6

    return time_in_seconds


def plotter(csv_file, data_array, main_title):
    df = pd.read_csv(csv_file)
    df['time'] = pd.to_datetime(df['time_stamp'])

    df['time'] = df['time'].apply(extract_seconds_from_timestamp)
    df['time'] = df['time'] - df['time'].min()  # shift time to zero



    num_of_plots = 6
    figure, axis = plt.subplots(3, 2, figsize=(10, 2*num_of_plots), sharex=True)
    figure.suptitle(main_title, fontsize=10)

    axis[0, 0].plot(np.array(df['time']), data_array[0])
    axis[0, 0].set_xlabel("time [s]")
    axis[0, 0].set_ylabel("Fx [N]")
    axis[0, 0].grid(True)

    axis[1, 0].plot(np.array(df['time']), data_array[1])
    axis[1, 0].set_xlabel("time [s]")
    axis[1, 0].set_ylabel("Fy [N]")
    axis[1, 0].grid(True)

    axis[2, 0].plot(np.array(df['time']), data_array[2])
    axis[2, 0].set_xlabel("time [s]")
    axis[2, 0].set_ylabel("Fz [N]")
    axis[2, 0].grid(True)

    axis[0, 1].plot(np.array(df['time']), data_array[3])
    axis[0, 1].set_xlabel("time [s]")
    axis[0, 1].set_ylabel("Tx [Nm]")
    axis[0, 1].grid(True)

    axis[1, 1].plot(np.array(df['time']), data_array[4])
    axis[1, 1].set_xlabel("time [s]")
    axis[1, 1].set_ylabel("Ty [Nm]")
    axis[1, 1].grid(True)

    axis[2, 1].plot(np.array(df['time']), data_array[5])
    axis[2, 1].set_xlabel("time [s]")
    axis[2, 1].set_ylabel("Tz [Nm]")
    axis[2, 1].grid(True)


    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
    plt.pause(0.001)


def plot_FT(csv_file_name):

    path_to_xdf_file = dir_to_save_data + "/csv_FT_data/"

    df = pd.read_csv(path_to_xdf_file + csv_file_name)

    # Extract actual joint currents
    Fx = np.array(df['Fx'])
    Fy = np.array(df['Fy'])
    Fz = np.array(df['Fz'])
    Tx = np.array(df['Tx'])
    Ty = np.array(df['Ty'])
    Tz = np.array(df['Tz'])
    FT_sensor = np.array([Fx, Fy, Fz, Tx, Ty, Tz])

    plotter(path_to_xdf_file, FT_sensor, main_title='Force-Torque sensor')



def plot_xdf_fabric_sensor(xdf_file_name):

    path_to_xdf_file = dir_to_save_data + "/xdf_files/"

    streams, header = pyxdf.load_xdf(path_to_xdf_file + xdf_file_name)

    for stream in streams:
        if stream["info"]["name"][0] == 'Sensor_mV':
            raw_xdf_voltages = stream["time_series"]
            raw_xdf_voltages = [float(item[0].strip('[]')) for item in raw_xdf_voltages]
            voltages_time_stamps =  stream["time_stamps"]

    plt.figure()
    plt.plot(voltages_time_stamps, raw_xdf_voltages, label="fabric_sensor")

    plt.title("fabric sensor (xdf)")
    plt.xlabel("time [s]")
    plt.ylabel("voltage [v]")
    plt.legend()
    plt.show()



def plot_csv_fabric_sensor(csv_file_name):

    path_to_xdf_file = dir_to_save_data + "/csv_fabric_sensor/"

    df = pd.read_csv(path_to_xdf_file + csv_file_name)

    header = df.columns.tolist()

    print(header)

    time = np.array(df[header[0]])
    values = np.array(df[header[1]])  # voltages (mV)

    plt.figure()
    plt.plot(time, values, label="fabric_sensor")

    plt.title("fabric sensor (csv)")
    plt.xlabel("time [s]")
    plt.ylabel("voltage [v]")
    plt.legend()
    plt.show()




if __name__ == "__main__":

    ## uncomment which function you want to plot.
    # plot_FT('test_ft_data_file.csv')
    # plot_xdf_fabric_sensor('gelsight_fabric_exp_3.xdf')
    plot_csv_fabric_sensor('slip_sensor_log3.csv')
    