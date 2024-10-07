''' ******************************************************************************
 * Project: plot
 * File: plotter.py
 * Author: Hamid Manouchehri
 * Email: hmanouch@buffalo.edu
 * Date: June 25, 2024
 *
 * Description:
 * This code is for plotting different data.
 *
 * License:
 * This code is licensed under the MIT License.
 * You may obtain a copy of the License at
 * 
 *     https://opensource.org/licenses/MIT
 *
 * SPDX-License-Identifier: MIT
 *
 * Disclaimer:
 * This software is provided "as is", without warranty of any kind, express or
 * implied, including but not limited to the warranties of merchantability,
 * fitness for a particular purpose, and noninfringement. In no event shall the
 * authors be liable for any claim, damages, or other liability, whether in an
 * action of contract, tort, or otherwise, arising from, out of, or in
 * connection with the software or the use or other dealings in the software.
 *
 ****************************************************************************** '''
#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyxdf
import yaml
from os.path import join, abspath, dirname
from scipy.fftpack import fft, ifft


gelsight_mini_interface_dir = dirname(abspath(__file__))  # WHATEVER/digit_FT_sensors/scripts
parent_dir = join(gelsight_mini_interface_dir, '..')
parent_dir_abs = abspath(parent_dir)
dir_to_config = join(parent_dir_abs, 'config', 'config.yml')
with open(dir_to_config, 'r') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)


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
    plt.show(block=False)
    plt.pause(0.001)


def plot_FT(csv_file_name):

    df = pd.read_csv(csv_file_name)

    # Extract actual joint currents
    Fx = np.array(df['Fx'])
    Fy = np.array(df['Fy'])
    Fz = np.array(df['Fz'])
    Tx = np.array(df['Tx'])
    Ty = np.array(df['Ty'])
    Tz = np.array(df['Tz'])
    FT_sensor = np.array([Fx, Fy, Fz, Tx, Ty, Tz])

    plotter(csv_file_name, FT_sensor, main_title='Force-Torque sensor')


def plot_csv_fabric_sensor(csv_file_name):

    df = pd.read_csv(csv_file_name)

    header = df.columns.tolist()

    time = np.array(df[header[0]])
    values = np.array(df[header[1]])  # voltages (mV)

    min_value = min(time)
    time_shifted_to_zero = [num - min_value for num in time]

    plt.figure()
    plt.plot(time, values, label="fabric_sensor")

    plt.title("fabric sensor (csv)", fontsize=15)
    plt.xlabel("time [s]", fontsize=15)
    plt.ylabel("voltage [v]", fontsize=15)
    plt.legend()
    plt.show(block=False)


def plot_ur5e_tool_lin_velocity(csv_file_name):

    df = pd.read_csv(csv_file_name)
    header = df.columns.tolist()
    time = np.array(df[header[0]])
    lin_vel_x = np.array(df[header[1]])
    lin_vel_y = np.array(df[header[2]])
    lin_vel_z = np.array(df[header[3]])

    ang_vel_x = np.array(df[header[4]])
    ang_vel_y = np.array(df[header[5]])
    ang_vel_z = np.array(df[header[6]])

    plt.plot(time, lin_vel_x, label="lin_vel_x")
    plt.plot(time, lin_vel_y, label="lin_vel_y")
    plt.plot(time, lin_vel_z, label="lin_vel_z")

    plt.title("UR5e actual tool velocity", fontsize=15)
    plt.xlabel("time [s]", fontsize=15)
    plt.ylabel("linear_velocity [m/s^2]", fontsize=15)
    plt.legend()
    plt.show(block=False)


def plot_img_velocity_estimation(csv_file_name):

    df = pd.read_csv(csv_file_name)

    header = df.columns.tolist()

    time = np.array(df[header[0]])[1:]
    vel = np.array(df[header[1]])[1:]  # discarding the first element (inf)

    plt.figure()

    # Perform FFT
    fft_signal = fft(vel)
    frequencies = np.fft.fftfreq(len(time), time[1] - time[0])

    cutoff = .5  # TODO
    fft_signal_filtered = np.where(np.abs(frequencies) > cutoff, 0, fft_signal)

    filtered_signal = ifft(fft_signal_filtered)

    plt.subplot(2, 1, 1)
    plt.plot(time, vel, label="vel")
    plt.xlabel("time [s]", fontsize=15)
    plt.ylabel("velocity from images [m/s^2]", fontsize=15)

    plt.subplot(2, 1, 2)
    plt.plot(time, np.real(filtered_signal), label="Filtered Signal")
    plt.xlabel("time [s]", fontsize=15)
    plt.ylabel("velocity after filtering [m/s^2]", fontsize=15)

    plt.show()


def plot_csv_ur5e_wrench(csv_file_name):

    df = pd.read_csv(csv_file_name)
    header = df.columns.tolist()
    time = np.array(df[header[0]])
    F_x = np.array(df[header[1]])
    F_y = np.array(df[header[2]])
    F_z = np.array(df[header[3]])

    T_x = np.array(df[header[4]])
    T_y = np.array(df[header[5]])
    T_z = np.array(df[header[6]])

    plt.plot(time, F_x, label="Force_x")
    plt.plot(time, F_y, label="Force_y")
    plt.plot(time, F_z, label="Force_z")

    plt.title("UR5e wrench (tools' FT)", fontsize=15)
    plt.xlabel("time [s]", fontsize=15)
    plt.ylabel("Force [N]", fontsize=15)
    plt.legend()
    plt.show(block=False)



def plot_various_data():
    
    df_est_vel = pd.read_csv(config["plotter"]["img_velocity_estimation"])
    # df_fabric = pd.read_csv(config["plotter"]["fabric_data"])
    df_time_synch_fabric = pd.read_csv(config["plotter"]["time_synched_fabric_data"])
    df_time_synched_ur5e_tool_velocity = pd.read_csv(config["plotter"]["time_synched_ur5e_tool_velocity"])
    df_time_synched_ur5e_wrench = pd.read_csv(config["plotter"]["time_synched_ur5e_wrench"])
    
    header_est_vel = df_est_vel.columns.tolist()
    time_est_vel = np.array(df_est_vel[header_est_vel[0]])[1:]
    est_vel = np.array(df_est_vel[header_est_vel[1]])[1:]  # discarding the first element (inf)

    header_time_synch_fabric = df_time_synch_fabric.columns.tolist()
    time_synch_fabric_time = np.array(df_time_synch_fabric[header_time_synch_fabric[0]])
    time_synch_fabric_voltage = np.array(df_time_synch_fabric[header_time_synch_fabric[1]])

    header_time_synch_ur5e_tool_velocity = df_time_synched_ur5e_tool_velocity.columns.tolist()
    time_synch_ur5e_tool_velocity_time = np.array(df_time_synched_ur5e_tool_velocity[header_time_synch_ur5e_tool_velocity[0]])
    time_synch_ur5e_tool_velocity = np.array(df_time_synched_ur5e_tool_velocity[header_time_synch_ur5e_tool_velocity[1]])

    header_time_synch_ur5e_wrench = df_time_synched_ur5e_wrench.columns.tolist()
    time_synch_ur5e_wrench_time = np.array(df_time_synched_ur5e_wrench[header_time_synch_ur5e_wrench[0]])
    time_synch_ur5e_wrench = np.array(df_time_synched_ur5e_wrench[header_time_synch_ur5e_wrench[1]])

    
    # Perform FFT
    fft_est_vel = fft(est_vel)
    est_vel_frequencies = np.fft.fftfreq(len(time_est_vel), time_est_vel[1] - time_est_vel[0])
    cutoff = 1  # TODO
    fft_signal_filtered = np.where(np.abs(est_vel_frequencies) > cutoff, 0, fft_est_vel)
    filtered_est_vel = ifft(fft_signal_filtered)

    plt.figure()

    plt.subplot(4, 1, 1)
    plt.plot(time_synch_ur5e_wrench_time, time_synch_ur5e_wrench,'b-.')
    plt.ylabel("ur5e tool force [N]", fontsize=8)

    plt.subplot(4, 1, 2)
    plt.plot(time_synch_ur5e_tool_velocity_time, time_synch_ur5e_tool_velocity,'b-.')
    plt.ylabel("ur5e tool linear vel [m/s^2]", fontsize=8)

    plt.subplot(4, 1, 3)
    plt.plot(time_synch_fabric_time, time_synch_fabric_voltage,'b-.')
    plt.ylabel("synched voltage [v]", fontsize=8)

    plt.subplot(4, 1, 4)
    plt.plot(time_est_vel, est_vel,'b-.')
    plt.ylabel("estimated velocity (gelsight) [m/s^2]", fontsize=8)

    # plt.subplot(4, 1, 5)
    # plt.plot(time_est_vel, np.real(filtered_est_vel),'b-.')
    # plt.xlabel("time [s]", fontsize=8)
    # plt.ylabel("filtered estimated velocity [m/s^2]", fontsize=8)

    # plt.tight_layout()
    plt.subplots_adjust(hspace=0.3)  # Increase the vertical spacing
    plt.show()




if __name__ == "__main__":

    ## uncomment which function you want to plot.
    # plot_csv_fabric_sensor(config["plotter"]["fabric_data"])
    # plot_img_velocity_estimation(config["plotter"]["img_velocity_estimation"])
    # plot_csv_ur5e_wrench(config["plotter"]["ur5e_wrench"])
    # plot_ur5e_tool_lin_velocity(config["plotter"]["ur5e_tool_velocity"])

    plot_various_data()
    
    plt.show()  # simultaneaus plotting