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
import sys
from os import getcwd, makedirs
from os.path import join, abspath 
import h5py
import numpy as np
import time
import select
from pynput import keyboard
from gelsight import gsdevice 


class GelsightMiniClass:
    # Class attribute (shared by all instances of the class)
    sensor = gsdevice.Camera("GelSight Mini")
    sensor.connect()

    gelsight_mini_interface_dir = getcwd()  # WHATEVER/digit_FT_sensors/scripts
    parent_dir = join(gelsight_mini_interface_dir, '..')  # Go one level up from the current_dir
    parent_dir_abs = abspath(parent_dir)
    dir_to_save_img = join(parent_dir_abs, 'data/img_data/')

    def __init__(self, hdf5_file_name):
        # Instance attribute (unique to each instance of the class)
        self.hdf5_file_name = hdf5_file_name


    def save_png_image(cls, dir, image_name):
        ''' Read the gelsight camera and capture the image. '''
        cls.sensor.get_image()
        cls.sensor.save_image(dir + image_name)
        
    
    def show_image(cls):

        while cls.sensor.while_condition:

            f1 = cls.sensor.get_image()
            bigframe = cv2.resize(f1, (f1.shape[0]*2, f1.shape[1]*2))
            cv2.imshow('Image', bigframe)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    
    def on_press(self, key):
        try:
            if key.char == 'q':
                return False  # This will stop the listener
        except AttributeError:
            pass  # Handle special keys (like ctrl, alt, etc.)



    def save_img_in_hdf5(self):
        ''' INPUT: is an instance attribute to defining name of hdf5 file to save images. '''

        print("Start recording images from gelsight-mini (press q to stop)...")

        imgs = []
        resp_time = []

        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        start_time = time.time()

        while listener.running:
            img = self.sensor.get_image()
            imgs.append(img)

            # end_time = time.time()
            # resp_time.append(end_time - start_time)
            # start_time = end_time
            
        average_time = sum(resp_time) / len(resp_time)
        print("average time: ", average_time)

        print("\nrecording images stopped...")

        imgs = np.array(imgs)

        with h5py.File(self.dir_to_save_img + self.hdf5_file_name, 'w') as f:
            f.create_dataset('images', data=imgs, compression='gzip', compression_opts=5)


    def save_hdf5_as_png(self):
        ''' 
        For post processing.
        INPUT: is an instance attribute to defining name of hdf5 file to save images.
        '''

        print("Post processing; saving hdf5 image data into '.png'...")

        save_images_dir = join(self.dir_to_save_img, self.hdf5_file_name.replace(".h5", ""))
        makedirs(save_images_dir, exist_ok=True)  # create the directory for .png images if does not exist.

        with h5py.File(self.dir_to_save_img + self.hdf5_file_name, 'r') as f:
                img_array = f['images'][:] 

        for i, image_data in enumerate(img_array):
            # Convert the image data to uint8 if necessary
            image_data = np.array(image_data, dtype=np.uint8)
            image_name = '/hdf5_image_' + str(i) + '.png'
            cv2.imwrite(save_images_dir + image_name, image_data)





    def do_cv_stuff(self, rgb_gelsight_image):

        grayScaledImg = cv2.cvtColor(rgb_gelsight_image, cv2.COLOR_RGB2GRAY)

        thresholdedImg = cv2.adaptiveThreshold(grayScaledImg ,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY_INV,21,4)
        
        thresholdedImg=cv2.medianBlur(thresholdedImg, 9)
        thresholdedImg=cv2.dilate(thresholdedImg, (3,3), iterations=2)
        thresholdedImg=cv2.medianBlur(thresholdedImg, 3)
        thresholdedImg=cv2.dilate(thresholdedImg, (3,3), iterations=2)

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresholdedImg , 8 , cv2.CV_32S)

        centroidLabeledImg = cv2.cvtColor(thresholdedImg,cv2.COLOR_GRAY2BGR)

        for i in range(len(stats)):
            stat = stats[i]
            x,y,w,h,area = stat
            if area < 100:
                centroidLabeledImg[y:y+h,x:x+w]=0

        for i in range(len(stats)):
            stat = stats[i]
            x,y,w,h,area = stat

            if area != np.max(stats[:,4]): # background pixel intensity is the largest area in stats
                if area > 55:
                    cv2.rectangle(centroidLabeledImg,[x,y],[x+w,y+h], (255,0,0), 2)    # img, bbox starting corner, bbox ending corner, color, line thickness

                    x,y = centroids[i].astype(int)
                    
                    cv2.circle(centroidLabeledImg,(x,y),2,(0,0,255),2)


        # converting back to color so the bboxs are still in red
        grayScaledImg = cv2.cvtColor(grayScaledImg,cv2.COLOR_GRAY2BGR)
        thresholdedImg = cv2.cvtColor(thresholdedImg,cv2.COLOR_GRAY2BGR)
        imgH = np.hstack((rgb_gelsight_image,grayScaledImg,thresholdedImg,centroidLabeledImg))
        # imgH = imgC


        cv2.imshow('connected component',imgH)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            print('quitting program')
            exit()
    




if __name__ == '__main__':

    gelsight_mini_obj = GelsightMiniClass('test.h5')

    # gelsight_mini_obj.show_image()

    while True:
        f1 = gelsight_mini_obj.sensor.get_image()
        # start = time.time()
        # gelsight_mini_obj.do_cv_stuff(f1)
        # end = time.time()
        # print(end - start)

    # gelsight_mini_obj.save_png_image(gelsight_mini_obj.dir_to_save_img, 'test_img.png')

    # gelsight_mini_obj.save_img_in_hdf5()
    # gelsight_mini_obj.save_hdf5_as_png()
