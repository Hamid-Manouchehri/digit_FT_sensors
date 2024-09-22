# gelsight_mini

Python scripts working with gelsight mini sensor, recording data and doing some analysis.

## Table of Contents
- [Project Structure](#project-structure)
- [scripts](#scripts)
- [src_main](#src_main)
- [Lab Streaming Layer](#lab-streaming-layer)

## Project Structure

```bash
digit_FT_sensors/
├── README.md
├── config/
│   └── config.yml                     # includes directory to various files.
│
├── bin/                               # include executable files for reading from RFT44-SB01 sensor
├── build/
│
├── data/
│   ├── csv_FT_data/                   # includes RFT44-SB01 sensor's data
│   │   └── ...
│   ├── csv_fabric_sensor/             # includes fabric sensor's data
│   │   └── ...
│   ├── img_data/                      # includes gelsight_mini sensor's data (images & csv files)
│   │   ├── img_csv_files/             # includes all csv files related to gelsight_mini sensor.
│   │   └── ...
│   └── xdf_files/                     # includes xdf files (Lab Streaming Layer), multiple sensors pushing data in a files + time samples
│       └── ...
│
├── scripts/                           
│   ├── data_logger_methods.py         # methods for reading a saving csv files
│   ├── gelsight_mini_interface.py     # methods for working with gelsight_mini sensor
│   ├── lsl_gelsight.py                # pushing gelsight_mini data to LSL
│   ├── slip_detection.py
│   ├── xdf_post_processing.py         # (script.1)
│   ├── velocity_estimation.py         # (script.2) estimation of velocity of object via analysing gelsight_mini images
│   └── plotter.py                     # (script.3) plotting csv files
│   
├── src_main/                          # RFT44-SB01 sensor
│   ├── FT_sensor.cpp                  # reading force-torque data from RFT44-SB01 sensor
│   └── LSL_FT.cpp                     # pushing RFT44-SB01 sensor data to LSL
│
└── CMakeLists.txt                     # configuring for building RFT44-SB01 sensor driver
```

## scripts
considering you have a xdf file in the proper dir (/data/xdf_files/) and editting `config.yml` file for proper refering, you will need to first run `xdf_post_processing.py`
to extract data (images & shear forces from fabric sensor and time stamps). After that, you can either plot the data (`plotter.py`) or if you need to estimate the velocity
via gelsight_mini images, executer `velocity_estimation.py`.
* NOTE: Remember `plotter.py` relies on .csv files, you might need to provide those files first and address them in `config.yml` file.

### xdf_post_processing.py
- Extracting images from gelsight_mini and dumping them in a specific folder which is addressed in `config.yml`.
- Iterating through images which are saved in the xdf file.
- Save time samples.
- Synchronizing sensory data.

## src_main
To build RFT44-SB01 sensor firmware, remove the current `/build` directory, then run the following command in `digit_FT_sensors/`:

``` 
cmake CMakeLists.txt -Bbuild 
```

* NOTE: for any changes in .cpp files (sensor firmware), you need to compile the code, so cd to `/build`, then run `make` command.

## Lab Streaming Layer

1. Connect all the computers and sensors to a host computer which is running LSL.
2. Run all the sensors.
3. Open up LSL software (Lab Recorder)
4. Check if all the sensors are showing there.
5. Tap start button to push sensory data in an xdf file.

* NOTE: You need `pylsl` for python and `lsl_cpp.h` libraries to be able to pushing sensory data on LSL.
