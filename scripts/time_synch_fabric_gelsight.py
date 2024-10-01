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

import cv2
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

    df_est_vel = pd.read_csv(estimated_vel)
    est_vel_header = df_est_vel.columns.tolist()
    est_vel_time = np.array(df_est_vel[est_vel_header[0]])
    est_vel = np.array(df_est_vel[est_vel_header[1]])

    df_fabric_data = pd.read_csv(fabric_data)
    fabric_header = df_fabric_data.columns.tolist()
    fabric_time = np.array(df_fabric_data[fabric_header[0]])
    fabric_voltage = np.array(df_fabric_data[fabric_header[1]])
    
    time_synched_fabric_fieldnames = ['time', 'voltage']  # TODO
    setup_csv(config["time_synch_fabric_gelsight"]["time_synched_fabric_data"], time_synched_fabric_fieldnames)
    
    # print("time", est_vel_time[1], " estimated_vel: ", est_vel[1])

    init_index_fabric = np.where(np.abs(fabric_time - est_vel_time[0]) == np.abs(fabric_time - est_vel_time[0]).min())
    closest_init_fabric_time = fabric_time[init_index_fabric][0]
    final_index_fabric = np.where(np.abs(fabric_time - est_vel_time[-1]) == np.abs(fabric_time - est_vel_time[-1]).min())
    closest_final_fabric_time = fabric_time[final_index_fabric][0]

    # for vel_time in est_vel_time:

    #     index = np.where(np.abs(fabric_time - vel_time) == np.abs(fabric_time - vel_time).min())
    #     closest_fabric_time = fabric_time[index][0]
    #     closest_fabric_voltage = fabric_voltage[index][0]
    #     print(" index: ", index[0][0], ", value: ", closest_fabric_time)

    #     data = {
    #         time_synched_fabric_fieldnames[0]: closest_fabric_time,
    #         time_synched_fabric_fieldnames[1]: closest_fabric_voltage
    #     }

    #     row = [data[time_synched_fabric_fieldnames[0]]] + [data[time_synched_fabric_fieldnames[1]]]
    #     save_to_csv(config["time_synch_fabric_gelsight"]["time_synched_fabric_data"], row)


    for i in range(init_index_fabric[0][0], final_index_fabric[0][0]):

        data = {
            time_synched_fabric_fieldnames[0]: fabric_time[i],
            time_synched_fabric_fieldnames[1]: fabric_voltage[i]
        }

        row = [data[time_synched_fabric_fieldnames[0]]] + [data[time_synched_fabric_fieldnames[1]]]
        save_to_csv(config["time_synch_fabric_gelsight"]["time_synched_fabric_data"], row)

        


