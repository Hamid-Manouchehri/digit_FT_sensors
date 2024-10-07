''' ******************************************************************************
 * Project: LSL configuration for gelsight mini Sensor
 * File: xdf_post_processing.py
 * Author: Hamid Manouchehri
 * Email: hmanouch@buffalo.edu
 * Date: August 20, 2024
 *
 * Description:
 * This code is for post processing of .xdf files.
 * NOTE: AFTER starting all the sensors, start Labrecorder and BEFORE stopping 
 * all the sensors, stop Labrecorder.
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
import ast
import re
import numpy as np
import yaml
import time
import pyxdf
from os import makedirs
from os.path import join, abspath, dirname
from data_logger_methods import setup_csv, save_to_csv


gelsight_mini_interface_dir = dirname(abspath(__file__))  # WHATEVER/digit_FT_sensors/scripts
parent_dir = join(gelsight_mini_interface_dir, '..')
parent_dir_abs = abspath(parent_dir)
dir_to_config = join(parent_dir_abs, 'config', 'config.yml')
with open(dir_to_config, 'r') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)


def show_xdf_images(raw_images):

    print("****************************")
    print("press 'q' to quit")
    print('Any key to see frames')
    print("****************************")

    img_width = 320
    img_height = 240
    rgb_channels = 3

    for img in raw_images:
        i = np.reshape(img, (img_height, img_width, rgb_channels)).astype('uint8')
        cv2.imshow('each image', i)
        
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            print('quitting program')
            break  # Exit the loop to quit the program
        elif key == ord('n'):
            continue  # Continue to the next image when 'n' is pressed

    cv2.destroyAllWindows()


def save_xdf_images(raw_images, file_path, folder_name):

    img_width = 320
    img_height = 240
    rgb_channels = 3

    img_name = 0

    new_folder_path = file_path + folder_name
    makedirs(new_folder_path, exist_ok=True)

    for img in raw_images:
        i = np.reshape(img, (img_height, img_width, rgb_channels)).astype('uint8')

        cv2.imwrite(new_folder_path + '/' + str(img_name) + '.jpg', i)

        img_name = img_name + 1


def save_img_time_stamps(img_time_stamps, file_path):

    index = 0
    fieldnames = ['index', 'time']
    setup_csv(file_path, fieldnames)

    for tm in img_time_stamps:

        data = {
            fieldnames[0]: index,
            fieldnames[1]: tm
        }

        row = [data[fieldnames[0]]] + [data[fieldnames[1]]]
        save_to_csv(file_path, row)

        index = index + 1


def save_xdf_fabric_sensor(voltage_time_stamp, voltage_data, file_path):

    fieldnames = ['time', 'voltage']
    setup_csv(file_path, fieldnames)

    for i in range(len(voltage_time_stamp)):

        data = {
            fieldnames[0]: voltage_time_stamp[i],
            fieldnames[1]: voltage_data[i]
        }

        row = [data[fieldnames[0]]] + [data[fieldnames[1]]]
        save_to_csv(file_path, row)


def save_xdf_ur5e_joint_states(ur5e_joint_states_time_stamp, ur5e_joint_states, file_path):

    fieldnames = ['time', 'shoulder_pan_pos', 'shoulder_lift_pos', 'elbow_pos', 'wrist1_pos', 'wrist2_pos', 'wrist3_pos',
                  'shoulder_pan_vel', 'shoulder_lift_vel', 'elbow_vel', 'wrist1_vel', 'wrist2_vel', 'wrist3_vel',
                  'shoulder_pan_curr', 'shoulder_lift_curr', 'elbow_curr', 'wrist1_curr', 'wrist2_curr', 'wrist3_curr']
    setup_csv(file_path, fieldnames)

    for i in range(len(ur5e_joint_states_time_stamp)):

        data = {
            fieldnames[0]: ur5e_joint_states_time_stamp[i],
            fieldnames[1]: ur5e_joint_states[i][0],
            fieldnames[2]: ur5e_joint_states[i][1],
            fieldnames[3]: ur5e_joint_states[i][2],
            fieldnames[4]: ur5e_joint_states[i][3],
            fieldnames[5]: ur5e_joint_states[i][4],
            fieldnames[6]: ur5e_joint_states[i][5],

            fieldnames[7]: ur5e_joint_states[i][6],
            fieldnames[8]: ur5e_joint_states[i][7],
            fieldnames[9]: ur5e_joint_states[i][8],
            fieldnames[10]: ur5e_joint_states[i][9],
            fieldnames[11]: ur5e_joint_states[i][10],
            fieldnames[12]: ur5e_joint_states[i][11],

            fieldnames[13]: ur5e_joint_states[i][12],
            fieldnames[14]: ur5e_joint_states[i][13],
            fieldnames[15]: ur5e_joint_states[i][14],
            fieldnames[16]: ur5e_joint_states[i][15],
            fieldnames[17]: ur5e_joint_states[i][16],
            fieldnames[18]: ur5e_joint_states[i][17]
        }

        row = [data[fieldnames[0]]] + \
              [data[fieldnames[1]]] + [data[fieldnames[2]]] + [data[fieldnames[3]]] + \
              [data[fieldnames[4]]] + [data[fieldnames[5]]] + [data[fieldnames[6]]] + \
              [data[fieldnames[7]]] + [data[fieldnames[8]]] + [data[fieldnames[9]]] + \
              [data[fieldnames[10]]] + [data[fieldnames[11]]] + [data[fieldnames[12]]] + \
              [data[fieldnames[13]]] + [data[fieldnames[14]]] + [data[fieldnames[15]]] + \
              [data[fieldnames[16]]] + [data[fieldnames[17]]] + [data[fieldnames[18]]]


        save_to_csv(file_path, row)


def save_xdf_ur5e_wrench(ur5e_wrench_time_stamp, ur5e_wrench, file_path):

    fieldnames = ['time', 'Fx', 'Fy', 'Fz', 'Tx', 'Ty', 'Tz']
    setup_csv(file_path, fieldnames)

    for i in range(len(ur5e_wrench_time_stamp)):

        data = {
            fieldnames[0]: ur5e_wrench_time_stamp[i],
            fieldnames[1]: ur5e_wrench[i][0],
            fieldnames[2]: ur5e_wrench[i][1],
            fieldnames[3]: ur5e_wrench[i][2],

            fieldnames[4]: ur5e_wrench[i][3],
            fieldnames[5]: ur5e_wrench[i][4],
            fieldnames[6]: ur5e_wrench[i][5]
        }

        row = [data[fieldnames[0]]] + \
              [data[fieldnames[1]]] + [data[fieldnames[2]]] + [data[fieldnames[3]]] + \
              [data[fieldnames[4]]] + [data[fieldnames[5]]] + [data[fieldnames[6]]]


        save_to_csv(file_path, row)


def save_xdf_ur5e_tool_coordinate(ur5e_tool_coordinate_time_stamp, ur5e_tool_coordinate, file_path):

    fieldnames = ['time', 'trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'rot_w']
    setup_csv(file_path, fieldnames)

    for i in range(len(ur5e_tool_coordinate_time_stamp)):

        data = {
            fieldnames[0]: ur5e_tool_coordinate_time_stamp[i],
            fieldnames[1]: ur5e_tool_coordinate[i][0],
            fieldnames[2]: ur5e_tool_coordinate[i][1],
            fieldnames[3]: ur5e_tool_coordinate[i][2],

            fieldnames[4]: ur5e_tool_coordinate[i][3],
            fieldnames[5]: ur5e_tool_coordinate[i][4],
            fieldnames[6]: ur5e_tool_coordinate[i][5],
            fieldnames[7]: ur5e_tool_coordinate[i][6]
        }

        row = [data[fieldnames[0]]] + \
              [data[fieldnames[1]]] + [data[fieldnames[2]]] + [data[fieldnames[3]]] + \
              [data[fieldnames[4]]] + [data[fieldnames[5]]] + [data[fieldnames[6]]] + \
              [data[fieldnames[7]]]


        save_to_csv(file_path, row)


def save_xdf_ur5e_tool_velocity(ur5e_tool_velocity_time_stamp, ur5e_tool_velocity, file_path):

    fieldnames = ['time', 'tool_vel_x', 'tool_vel_y', 'tool_vel_z', 'tool_ang_vel_x', 'tool_ang_vel_y', 'tool_ang_vel_z']
    setup_csv(file_path, fieldnames)

    for i in range(len(ur5e_tool_velocity_time_stamp)):

        data = {
            fieldnames[0]: ur5e_tool_velocity_time_stamp[i],
            fieldnames[1]: ur5e_tool_velocity[i][0],
            fieldnames[2]: ur5e_tool_velocity[i][1],
            fieldnames[3]: ur5e_tool_velocity[i][2],

            fieldnames[4]: ur5e_tool_velocity[i][3],
            fieldnames[5]: ur5e_tool_velocity[i][4],
            fieldnames[6]: ur5e_tool_velocity[i][5]
        }

        row = [data[fieldnames[0]]] + \
              [data[fieldnames[1]]] + [data[fieldnames[2]]] + [data[fieldnames[3]]] + \
              [data[fieldnames[4]]] + [data[fieldnames[5]]] + [data[fieldnames[6]]]


        save_to_csv(file_path, row)


        
if __name__ == '__main__':

    streams, header = pyxdf.load_xdf(config["xdf_post_processing"]["fabric_gelsight_xdf"])

    for stream in streams:
        if stream["info"]["name"][0] == 'GelSightMini':
            raw_xdf_images = stream["time_series"]
            images_time_stamps =  stream["time_stamps"]  # time

        if stream["info"]["name"][0] == 'Sensor_mV':
            raw_xdf_voltages = stream["time_series"]
            raw_xdf_voltages = [float(item[0].strip('[]')) for item in raw_xdf_voltages]
            voltages_time_stamps =  stream["time_stamps"]  # time

        if stream["info"]["name"][0] == 'ur5e_joint_states':
            raw_xdf_ur5e_joint_states = stream["time_series"]
            ur5e_joint_states_time_stamps =  stream["time_stamps"]  # time

        if stream["info"]["name"][0] == 'ur5e_wrench':
            raw_xdf_ur5e_wrench = stream["time_series"]
            ur5e_wrench_time_stamps =  stream["time_stamps"]  # time

        if stream["info"]["name"][0] == 'ur5e_tool_coordinate':
            raw_xdf_ur5e_tool_coordinate = stream["time_series"]
            ur5e_tool_coordinate_time_stamps =  stream["time_stamps"]  # time

        if stream["info"]["name"][0] == 'ur5e_tool_velocity':
            raw_xdf_ur5e_tool_velocity = stream["time_series"]
            ur5e_tool_velocity_time_stamps =  stream["time_stamps"]  # time



    # save_img_time_stamps(images_time_stamps, config["xdf_post_processing"]["img_frame_times"])
    # save_xdf_images(raw_xdf_images, config["xdf_post_processing"]["img_data"], folder_name="fabric_gelsight_test_2")

    # save_xdf_fabric_sensor(voltages_time_stamps, raw_xdf_voltages, config["xdf_post_processing"]["fabric_data"])

    # save_xdf_ur5e_joint_states(ur5e_joint_states_time_stamps, raw_xdf_ur5e_joint_states, config["xdf_post_processing"]["ur5e_joint_states"])
    # save_xdf_ur5e_wrench(ur5e_wrench_time_stamps, raw_xdf_ur5e_wrench, config["xdf_post_processing"]["ur5e_wrench"])

    # save_xdf_ur5e_tool_coordinate(ur5e_tool_coordinate_time_stamps, raw_xdf_ur5e_tool_coordinate, config["xdf_post_processing"]["ur5e_tool_coordinate"])
    # save_xdf_ur5e_tool_velocity(ur5e_tool_velocity_time_stamps, raw_xdf_ur5e_tool_velocity, config["xdf_post_processing"]["ur5e_tool_velocity"])