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
import h5py
import numpy as np
import time
from gelsight import gsdevice 


class GelsightMiniClass:
    # Class attribute (shared by all instances of the class)
    sensor = gsdevice.Camera("GelSight Mini")
    sensor.connect()

    current_dir = getcwd()
    parent_dir = join(current_dir, '..')  # Go one level up from the current_dir
    parent_dir_abs = abspath(parent_dir)
    dir_to_save_img = join(parent_dir_abs, 'data/img_data/')

    def __init__(self, instance_attribute):
        # Instance attribute (unique to each instance of the class)
        self.instance_attribute = instance_attribute


    # Instance method (can access instance attributes)
    def save_png_image(cls, image_name='test_img.png'):

        cls.sensor.get_image()
        cls.sensor.save_image(cls.dir_to_save_img + image_name)

    
    def show_image(cls):

        while cls.sensor.while_condition:

            f1 = cls.sensor.get_image()
            bigframe = cv2.resize(f1, (f1.shape[0]*2, f1.shape[1]*2))
            cv2.imshow('Image', bigframe)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



    def save_img_in_hdf5(cls, hdf5_file_name='test.h5'):

        imgs=[]

        for i in range(5):
            img = cls.sensor.get_image()
            imgs.append(img)

        imgs = np.array(imgs)

        with h5py.File(cls.dir_to_save_img + hdf5_file_name, 'w') as f:
            f.create_dataset('images', data=imgs, compression='gzip', compression_opts=5)
        


    def save_hdf5_as_png(cls, hdf5_file_name='test.h5'):

        with h5py.File(cls.dir_to_save_img + hdf5_file_name, 'r') as f:
                img_array = f['images'][:] 

        # print(np.shape(img_array))
        # print(img_array)

        for i, image_data in enumerate(img_array):
            # Convert the image data to uint8 if necessary
            image_data = np.array(image_data, dtype=np.uint8)

            ## showing each image separately:
            # cv2.imshow(f'Image {i+1}', image_data)
            # print(f"Press any key to continue to the next image ({i+1}/{img_array.shape[0]})...")
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            cls.save_png_image('hdf5_image_' + str(i) + '.png')



if __name__ == '__main__':

    gelsight_mini_obj = GelsightMiniClass('hello')

    # gelsight_mini_obj.save_img_in_hdf5()

    gelsight_mini_obj.save_hdf5_as_png()