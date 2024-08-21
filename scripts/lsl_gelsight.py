''' ******************************************************************************
 * Project: LSL configuration for gelsight mini Sensor
 * File: lsl_gelsight.py
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
from os import getcwd
from os.path import join, abspath
from pylsl import StreamInfo, StreamOutlet
from gelsight import gsdevice




if __name__ == '__main__':

    sensor = gsdevice.Camera("GelSight Mini")
    sensor.connect()

    # Define LSL stream
    info = StreamInfo('GelSightMini', 'Video', 1, 30, 'string')  # Adjust based on your data type
    outlet = StreamOutlet(info)

    # Stream data
    while True:
        frame = str(sensor.get_image())
        # print(frame)
        # print(np.shape(frame))
        outlet.push_sample([frame])

