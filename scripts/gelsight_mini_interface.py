''' ******************************************************************************
 * Project: gelsight mini Sensor Interface
 * File: gelsight_mini_interface.py
 * Author: Hamid Manouchehri
 * Email: hmanouch@buffalo.edu
 * Date: August 4, 2024
 *
 * Description:
 * This code interfaces with the gelsight mini sensor to read and record
 * image data at a specified frequency.
 *
 * License:
 * This code is licensed under the MIT License.
 * You may obtain a copy of the License at
 * 
 *     https://opensource.org/licenses/MIT
 *
 * SPDX-License-Identifier: MIT
 *
 * Usage:
 * Compile the code using a C++ compiler and run the executable. Ensure that the
 * sensor is connected to the specified serial port.
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
from os import getcwd
from os.path import join, abspath 
from gelsight import gsdevice


img_name = 'img1.png'  # TODO

current_dir = getcwd()
parent_dir = join(current_dir, '..')  # Go one level up from the current_dir
parent_dir_abs = abspath(parent_dir)
dir_to_save_img = join(parent_dir_abs, 'data/img_data')


def show_image(sensor):

    while sensor.while_condition:

        # get the roi image
        f1 = sensor.get_image()
        # if USE_ROI:
        #     f1 = f1[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        bigframe = cv2.resize(f1, (f1.shape[0]*2, f1.shape[1]*2))
        cv2.imshow('Image', bigframe)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def main():
    sensor = gsdevice.Camera("GelSight Mini")

    sensor.connect()
    # show_image(sensor)

    sensor.get_image()
    sensor.save_image(dir_to_save_img + '/' + img_name)

    

if __name__ == '__main__':
    main()