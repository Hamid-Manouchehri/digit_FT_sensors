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

    streams, header = pyxdf.load_xdf(join(dir_to_save_img_csv_files, xdf_file_name))

    for stream in streams:
        print(stream['info']['name'][0])  # Access the name of each stream

    # You can also print other details of the streams if needed
    # print("header: \n", header, '\n')
    # print("streams: \n", streams)
