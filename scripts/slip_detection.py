''' ******************************************************************************
 * Project: gelsight mini Sensor Interface
 * File: slip_detection.py
 * Author: Hamid Manouchehri
 * Email: hmanouch@buffalo.edu
 * Date: August 15, 2024
 *
 * Description:
 * This code interfaces with the gelsight mini sensor to detect slip in object.
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
import numpy as np
import time
from gelsight import gsdevice 

    
sensor = gsdevice.Camera("GelSight Mini")
sensor.connect()

img_buff = []
thresholded_value = 5  # TODO; The less, the more sensitive 


if __name__ == '__main__':

    img_buff = sensor.get_image()
    img_buff = cv2.cvtColor(img_buff, cv2.COLOR_BGR2GRAY)

    while True:

        start = time.time()
        img_gray = sensor.get_image()
        end = time.time()
        # print("elapsed time: ", end - start)

        start = time.time()
        img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
        end = time.time()
        print("gray scale time: ", end - start)

        start = time.time()
        difference = cv2.absdiff(img_buff, img_gray)
        end = time.time()
        # print("calc diff img: ", end - start)

        img_buff = img_gray

        _, thresholded_diff = cv2.threshold(difference, thresholded_value, 255, cv2.THRESH_BINARY)

        # Calculate the number of differing pixels
        non_zero_count = np.count_nonzero(thresholded_diff)

        if non_zero_count == 0:
            print("The images are identical.")

        else:
            print(f"The images have {non_zero_count} differing pixels.")
            
            # cv2.imshow('Difference', difference)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
    
