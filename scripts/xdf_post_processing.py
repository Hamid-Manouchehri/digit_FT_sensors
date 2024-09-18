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


img_folder_name = "fabric_gelsight_v13"  # TODO

gelsight_mini_interface_dir = dirname(abspath(__file__))  # WHATEVER/digit_FT_sensors/scripts
parent_dir = join(gelsight_mini_interface_dir, '..')
parent_dir_abs = abspath(parent_dir)
dir_to_config = join(parent_dir_abs, 'config', 'config.yml')
with open(dir_to_config, 'r') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)


fieldnames = ['index', 'time']  # TODO
setup_csv(config["xdf_post_processing"]["img_frame_times"], fieldnames)

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


def save_xdf_images(folder_name, raw_images):

    img_width = 320
    img_height = 240
    rgb_channels = 3

    img_name = 0

    new_folder_path = config["xdf_post_processing"]["img_data_dir"] + folder_name
    makedirs(new_folder_path, exist_ok=True)

    for img in raw_images:
        i = np.reshape(img, (img_height, img_width, rgb_channels)).astype('uint8')

        cv2.imwrite(new_folder_path + '/' + str(img_name) + '.jpg', i)

        img_name = img_name + 1


def save_img_time_stamps(img_time_stamps):

    index = 0

    for tm in img_time_stamps:

        data = {
            fieldnames[0]: index,
            fieldnames[1]: tm
        }

        row = [data[fieldnames[0]]]  + [data[fieldnames[1]]]
        save_to_csv(config["xdf_post_processing"]["img_frame_times"], row)

        index = index + 1



if __name__ == '__main__':

    streams, header = pyxdf.load_xdf(config["xdf_post_processing"]["fabric_gelsight_xdf"])

    for stream in streams:
        if stream["info"]["name"][0] == 'GelSightMini':
            raw_xdf_images = stream["time_series"]
            images_time_stamps =  stream["time_stamps"]

        if stream["info"]["name"][0] == 'Sensor_mV':
            raw_xdf_voltages = stream["time_series"]
            raw_xdf_voltages = [float(item[0].strip('[]')) for item in raw_xdf_voltages]
            voltages_time_stamps =  stream["time_stamps"]

    # print(len(images_time_stamps))
    # show_xdf_images(raw_xdf_images)  
    save_img_time_stamps(images_time_stamps)
    # save_xdf_images(img_folder_name, raw_xdf_images)

    ## time synchronization:
    if len(images_time_stamps) <= len(voltages_time_stamps):
        ## Interpolating voltage data to image time points
        interpolated_voltage_data = np.interp(images_time_stamps, voltages_time_stamps, raw_xdf_voltages)
        sync_time = images_time_stamps

    else:
        ## Interpolating image data to voltage time points
        interpolated_gelsight_data = np.interp(voltages_time_stamps, images_time_stamps, raw_xdf_images)
        sync_time = voltages_time_stamps

