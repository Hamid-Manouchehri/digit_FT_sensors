''' ******************************************************************************
 * Project: LSL configuration for gelsight mini Sensor
 * File: time_synch_fabric_gelsight.py
 * Author: Hamid Manouchehri
 * Email: hmanouch@buffalo.edu
 * Date: October 1, 2024
 *
 * Description:
 * Synchronizing fabric sensor time to gelsight-mini
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

import numpy as np
import cv2
import yaml
from os.path import join, abspath, dirname
import pandas as pd
from data_logger_methods import setup_csv, save_to_csv

gelsight_mini_interface_dir = dirname(abspath(__file__))  # WHATEVER/digit_FT_sensors/scripts
parent_dir = join(gelsight_mini_interface_dir, '..')
parent_dir_abs = abspath(parent_dir)
dir_to_config = join(parent_dir_abs, 'config', 'config.yml')
with open(dir_to_config, 'r') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

if __name__ == '__main__':

    estimated_vel = config["time_synch_fabric_gelsight"]["img_velocity_estimation"]

    fabric_data = config["time_synch_fabric_gelsight"]["fabric_data"]
    ur5e_tool_velocity = config["time_synch_fabric_gelsight"]["ur5e_tool_velocity"]
    ur5e_wrench = config["time_synch_fabric_gelsight"]["ur5e_wrench"]

    df_est_vel = pd.read_csv(estimated_vel)
    est_vel_header = df_est_vel.columns.tolist()
    est_vel_time = np.array(df_est_vel[est_vel_header[0]])
    est_vel = np.array(df_est_vel[est_vel_header[1]])

    time_synched_fabric_fieldnames = ['time', 'voltage']  # TODO
    df_fabric_data = pd.read_csv(fabric_data)
    fabric_header = df_fabric_data.columns.tolist()
    fabric_time = np.array(df_fabric_data[fabric_header[0]])
    fabric_voltage = np.array(df_fabric_data[fabric_header[1]])

    time_synched_ur5e_tool_velocity_fieldnames = ['time', 'tool_vel_y']  # TODO
    df_ur5e_tool_velocity = pd.read_csv(ur5e_tool_velocity)
    ur5e_tool_velocity_header = df_ur5e_tool_velocity.columns.tolist()
    ur5e_tool_velocity_time = np.array(df_ur5e_tool_velocity[ur5e_tool_velocity_header[0]])
    ur5e_tool_velocity = np.array(df_ur5e_tool_velocity[ur5e_tool_velocity_header[2]])  # tool_vel_y

    time_synched_ur5e_wrench_fieldnames = ['time', 'Fy']  # TODO
    df_ur5e_wrench = pd.read_csv(ur5e_wrench)
    ur5e_wrench_header = df_ur5e_wrench.columns.tolist()
    ur5e_wrench_time = np.array(df_ur5e_wrench[ur5e_wrench_header[0]])
    ur5e_wrench = np.array(df_ur5e_wrench[ur5e_wrench_header[2]])  # Fy
    

    init_index_fabric = np.where(np.abs(fabric_time - est_vel_time[0]) == np.abs(fabric_time - est_vel_time[0]).min())
    final_index_fabric = np.where(np.abs(fabric_time - est_vel_time[-1]) == np.abs(fabric_time - est_vel_time[-1]).min())

    init_index_ur5e_tool_velocity = np.where(np.abs(ur5e_tool_velocity_time - est_vel_time[0]) == np.abs(ur5e_tool_velocity_time - est_vel_time[0]).min())
    final_index_ur5e_tool_velocity = np.where(np.abs(ur5e_tool_velocity_time - est_vel_time[-1]) == np.abs(ur5e_tool_velocity_time - est_vel_time[-1]).min())

    init_index_ur5e_wrench = np.where(np.abs(ur5e_wrench_time - est_vel_time[0]) == np.abs(ur5e_wrench_time - est_vel_time[0]).min())
    final_index_ur5e_wrench = np.where(np.abs(ur5e_wrench_time - est_vel_time[-1]) == np.abs(ur5e_wrench_time - est_vel_time[-1]).min())


    # setup_csv(config["time_synch_fabric_gelsight"]["time_synched_fabric_data"], time_synched_fabric_fieldnames)
    # for i in range(init_index_fabric[0][0], final_index_fabric[0][0]):

    #     data = {
    #         time_synched_fabric_fieldnames[0]: fabric_time[i],
    #         time_synched_fabric_fieldnames[1]: fabric_voltage[i]
    #     }

    #     row = [data[time_synched_fabric_fieldnames[0]]] + [data[time_synched_fabric_fieldnames[1]]]
    #     save_to_csv(config["time_synch_fabric_gelsight"]["time_synched_fabric_data"], row)


    # setup_csv(config["time_synch_fabric_gelsight"]["time_synched_ur5e_tool_velocity"], time_synched_ur5e_tool_velocity_fieldnames)
    # for i in range(init_index_ur5e_tool_velocity[0][0], final_index_ur5e_tool_velocity[0][0]):

    #     data = {
    #         time_synched_ur5e_tool_velocity_fieldnames[0]: ur5e_tool_velocity_time[i],
    #         time_synched_ur5e_tool_velocity_fieldnames[1]: ur5e_tool_velocity[i]
    #     }

    #     row = [data[time_synched_ur5e_tool_velocity_fieldnames[0]]] + [data[time_synched_ur5e_tool_velocity_fieldnames[1]]]
    #     save_to_csv(config["time_synch_fabric_gelsight"]["time_synched_ur5e_tool_velocity"], row)


    # setup_csv(config["time_synch_fabric_gelsight"]["time_synched_ur5e_wrench"], time_synched_ur5e_wrench_fieldnames)
    # for i in range(init_index_ur5e_wrench[0][0], final_index_ur5e_wrench[0][0]):

    #     data = {
    #         time_synched_ur5e_wrench_fieldnames[0]: ur5e_wrench_time[i],
    #         time_synched_ur5e_wrench_fieldnames[1]: ur5e_wrench[i]
    #     }

    #     row = [data[time_synched_ur5e_wrench_fieldnames[0]]] + [data[time_synched_ur5e_wrench_fieldnames[1]]]
    #     save_to_csv(config["time_synch_fabric_gelsight"]["time_synched_ur5e_wrench"], row)


