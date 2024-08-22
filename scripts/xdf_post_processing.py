''' ******************************************************************************
 * Project: LSL configuration for gelsight mini Sensor
 * File: xdf_post_processing.py
 * Author: Hamid Manouchehri
 * Email: hmanouch@buffalo.edu
 * Date: August 20, 2024
 *
 * Description:
 * This code is for post processing of .xdf files.
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
import time
import pyxdf
from os import getcwd
from os.path import join, abspath

xdf_file_name = 'gelsight_fabric_exp_2.xdf'  # TODO

gelsight_mini_interface_dir = getcwd()  # WHATEVER/digit_FT_sensors/scripts
parent_dir = join(gelsight_mini_interface_dir, '..')  # Go one level up from the current_dir
parent_dir_abs = abspath(parent_dir)
dir_to_save_img_csv_files = join(parent_dir_abs, 'data/xdf_files/')

if __name__ == '__main__':

    streams, header = pyxdf.load_xdf(dir_to_save_img_csv_files + xdf_file_name)

    # time_series => data
    # time_stamp => time

    for stream in streams:
        if stream["info"]["name"][0] == 'GelSightMini':
            raw_images = stream["time_series"]
            # raw_images = [float(item[0].strip('[]')) for item in raw_images[10][0]]
            images_time_stamps =  stream["time_stamps"]

        if stream["info"]["name"][0] == 'Sensor_mV':
            raw_voltages = stream["time_series"]
            raw_voltages = [float(item[0].strip('[]')) for item in raw_voltages]
            voltages_time_stamps =  stream["time_stamps"]

    # print(np.shape(raw_images[10][:]))
    # print(raw_images[10])
   
    print(images_time_stamps)


    cleaned_image_string = [s.replace('\n', '') for s in raw_images[10]]


    print(cleaned_image_string)
    
    cleaned_image_string = cleaned_image_string[0]  # Get the string from the list
    cleaned_image_string = re.sub(r'[\[\]]', '', cleaned_image_string)  # Remove brackets
    image_values = cleaned_image_string.split()  # Split string into a list of strings

    # Step 3: Convert the list of strings to a list of floats
    image_floats = [float(value) for value in image_values]

    print(image_floats)

    # print(cleaned_image_string) 
