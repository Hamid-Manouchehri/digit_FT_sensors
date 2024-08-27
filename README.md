## Notes: (Ubuntu 20.04)
1. Since data is not being tracked by the repo, wherever you clone the repository, create a `/data` directory including folders of `csv_FT_data`, `csv_fabric_sensor`, `img_data` and `xdf_files`.

2. Activate the conda environment while using python scripts: `conda activate CONDA_ENV_NAME`.

3. Lab Streaming Layer (LSL): First things first, install `pylsl` and `pyxdf`. You can connect (via Ethenet / USB) different computers (hosting various sensors (streaming data)) to one host computer in which LSL is setted up on.
Then install `LabRecorder`:
```
cd WHATEVER/App-LabRecorder/build
./LabRecorder
```
**NOTE:** Run all the sensors, then start LabRecorder to record all the data streams as an xdf file. When the recording is done, first stop LabRecorder then the sensors.
Inorder to validate if the data is saved correctly, use Matlab. Clone the required repository ([matlab-xdf](https://github.com/xdf-modules/xdf-Matlab)) and dump the xdf file in it, then in Matlab use the following command to load the xdf file:
```
load_xdf("xdf-file-name.xdf")
```
