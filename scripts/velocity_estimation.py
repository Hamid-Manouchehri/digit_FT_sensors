''' ******************************************************************************
 * Project: gelsight mini Sensor Interface
 * File: velocity_estimation.py
 * Author: Hamid Manouchehri
 * Email: hmanouch@buffalo.edu
 * Date: Sep 16, 2024
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
import cv2
import yaml
import math
from os.path import join, abspath, dirname
import pandas as pd


gelsight_mini_interface_dir = dirname(abspath(__file__))  # WHATEVER/digit_FT_sensors/scripts
parent_dir = join(gelsight_mini_interface_dir, '..')
parent_dir_abs = abspath(parent_dir)
dir_to_config = join(parent_dir_abs, 'config', 'config.yml')
with open(dir_to_config, 'r') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)


blob_dist_thresh = .5

def calc_vel_of_obj(current_centroids_list, prev_centroids_list, dt):

    min_euclidean_dist = np.inf
    sum_min_euclidean_dist = 0

    for current_point in current_centroids_list:
        for prev_point in prev_centroids_list:

            euclidean_dist = math.sqrt((current_point[0] - prev_point[0])**2 + (current_point[1] - prev_point[1])**2)

            min_euclidean_dist = min(min_euclidean_dist, euclidean_dist)

            # print("euclidean dist: ", euclidean_dist)
            # print()

        sum_min_euclidean_dist = sum_min_euclidean_dist + min_euclidean_dist

    print(sum_min_euclidean_dist)
    N = len(current_centroids_list)
    vel = 1 / N * (sum_min_euclidean_dist) / dt

    return vel


def do_cv_stuff(img1_path):

    current_centroids_list = []
    buf_centroids_list = []

    df = pd.read_csv(config['velocity_estimation']['img_frame_times'])

    index_frame_time = np.array(df['index'])
    frame_time = np.array(df['time'])

    for i in range(131, 165):

        img = img1_path + str(i) + ".jpg"

        # Read the image from the file path
        img1 = cv2.imread(img)
        
        if img1 is None:
            print(f"Error: Image not found at {img}")
            return

        # Convert the image to grayscale
        img2 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

        # Apply adaptive thresholding
        # img3 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 4)
        img3 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 81, 8)
        
        # Further processing steps
        img3 = cv2.medianBlur(img3, 9)
        img3 = cv2.dilate(img3, (3, 3), iterations=2)
        img3 = cv2.medianBlur(img3, 3)
        img3 = cv2.dilate(img3, (3, 3), iterations=2)

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img3, 8, cv2.CV_32S)

        imgC = cv2.cvtColor(img3, cv2.COLOR_GRAY2BGR)

        for i in range(len(stats)):
            stat = stats[i]
            x, y, w, h, area = stat

            if area != np.max(stats[:, 4]):  # Exclude background
                if area > 150:
                    cv2.rectangle(imgC, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    x, y = centroids[i].astype(int)
                    cv2.circle(imgC, (x, y), 2, (0, 0, 255), 2)
                    
                    current_centroids_list.append([x,y])

                    # print("area: ", area, "centroid: ", x, y)

        # print(centroids_list)
        # print()

        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        img3 = cv2.cvtColor(img3, cv2.COLOR_GRAY2BGR)
        imgH = np.hstack((img1, img2, img3, imgC))

        cv2.imshow('Processed Image', imgC)

        if not buf_centroids_list is False:
            delta_t = frame_time[i+1] - frame_time[i]
            vel = calc_vel_of_obj(current_centroids_list, buf_centroids_list, delta_t)

            print('vel: ', vel)

        buf_centroids_list = current_centroids_list
        current_centroids_list = []

        if cv2.waitKey(0) & 0xFF == ord('q'):
            print('Quitting program')
            exit()

        # cv2.waitKey(50)
        # cv2.destroyAllWindows()


if __name__ == '__main__':

    path_to_blobs = config["velocity_estimation"]["blob_img_dir"]

    do_cv_stuff(path_to_blobs)
