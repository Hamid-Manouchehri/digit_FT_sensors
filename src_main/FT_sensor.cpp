/******************************************************************************
 * Project: Force-Torque Sensor Interface
 * File: FT_sensor.cpp
 * Author: Hamid Manouchehri
 * Email: hmanouch@buffalo.edu
 * Date: August 4, 2024
 *
 * Description:
 * This code interfaces with the RFT44-SB01 force-torque sensor to read and record
 * force-torque data at a specified frequency. It initializes the sensor, sets the
 * communication parameters, and continuously reads the sensor data.
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
 ******************************************************************************/

#include <iostream>
#include <thread>
#include <chrono>
#include <string>
#include <iomanip>
#include <sstream>
#include <stdlib.h>
#include <stdio.h>
#include <fstream>
#include <unistd.h>
#include <limits.h> // For PATH_MAX
#include <yaml-cpp/yaml.h>
#include "robotous_ft/RFT_UART_SAMPLE.h"

// using namespace std;


const char* devName = "/dev/ttyUSB"; // Change to const char*
BYTE port = 0;  // TODO
DWORD baudRate = B115200;
DWORD byteSize = CS8;
int dataRateInterval = 10; // milliseconds, Example: 100 ms for 10 Hz, TODO


void initializeCSVFile(std::string csv_file){

	std::ofstream datafile;
    datafile.open(csv_file);
    datafile << "index,time_stamp,Fx,Fy,Fz,Tx,Ty,Tz\n";
    datafile.close();

}


std::string getCurrentTimeISO8601() {
    auto now = std::chrono::system_clock::now();
    auto now_time_t = std::chrono::system_clock::to_time_t(now);
    auto now_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;

    std::tm now_tm;
#if defined(_WIN32) || defined(_WIN64)
    localtime_s(&now_tm, &now_time_t);  // For Windows
#else
    localtime_r(&now_time_t, &now_tm);  // For POSIX
#endif

    std::ostringstream oss;
    oss << std::put_time(&now_tm, "%Y-%m-%dT%H:%M:%S") << '.' << std::setfill('0') << std::setw(3) << now_ms.count();
    return oss.str();
}


void SAVE_FT_TO_CSV_FILE(std::string csv_file, float FT_data[], int img_index){

	std::string time_stamp;
	std::ofstream datafile;

    datafile.open(csv_file, std::ios::app);

	time_stamp = getCurrentTimeISO8601();

    datafile << img_index << "," << time_stamp << "," << FT_data[0] << "," << FT_data[1] << "," << FT_data[2] << ","
                << FT_data[3] << "," << FT_data[4] << "," << FT_data[5] << "\n";


	datafile.close();

}


// Function to initialize and open the sensor port
bool initializeSensor(CRT_RFT_UART& sensor, const char* devName, BYTE port, DWORD baudRate, DWORD byteSize) {
    // Cast const char* to char*
    if (!sensor.openPort(const_cast<char*>(devName), port, baudRate, byteSize)) {
        std::cerr << "Failed to open port" << std::endl;
        return false;
    }
    return true;
}

// Function to set the data rate interval
bool setDataRate(CRT_RFT_UART& sensor, int dataRateInterval) {
    if (!sensor.set_FT_Cont_Interval(dataRateInterval)) {
        std::cerr << "Failed to set data rate interval" << std::endl;
        return false;
    }
    return true;
}

// Function to read and print FT data continuously at the specified frequency
void readAndPrintFTData(std::string csv_file, CRT_RFT_UART& sensor, int dataRateInterval) {
    
    sensor.set_FT_Bias(1);  // UNCOMMENT ONLY ONCE WHEN YOU REPLUG THE SENSOR, PORT NUMBER CHANGES

    sensor.rqst_FT_Continuous();
	int img_index = 0;

    while (true) {

        // sensor.rqst_FT_Continuous(); // UNCOMMENT ONLY ONCE WHEN YOU REPLUG THE SENSOR, PORT NUMBER CHANGES

        auto start = std::chrono::high_resolution_clock::now();
        float* FT_data = sensor.m_RFT_IF_PACKET.m_rcvdForce;
        auto end = std::chrono::high_resolution_clock::now();
        // auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        // std::cout << "Time taken by process: " << <std::float>duration.count() << " milliseconds" << std::endl;

        // std::chrono::duration<double> duration = end - start;
        // std::cout << "Time taken by process: " << duration.count() << " milliseconds" << std::endl;       


		// SAVE_FT_TO_CSV_FILE(csv_file, FT_data, img_index);  // TODO
        
		img_index += 1;

        // Print the FT data
        // std::cout << "Force-Torque Data: ";
        for (int i = 0; i < 6; ++i) {
            std::cout << FT_data[i];
            if (i < 5) std::cout << ", ";
        }
        std::cout << std::endl;


        std::this_thread::sleep_for(std::chrono::milliseconds(dataRateInterval));
    }
}

int main() {

    char cwd[PATH_MAX];  // current directory
    std::string full_path_to_FT_csv_file;
    YAML::Node config = YAML::LoadFile("../config/config.yaml");

    // Get the current working directory
    if (getcwd(cwd, sizeof(cwd)) != nullptr) {

        // Convert the C-style string to a C++ string for easier manipulation
        std::string current_dir(cwd);

        // Find the last slash in the path and remove everything after it
        std::size_t pos = current_dir.find_last_of('/');
        if (pos != std::string::npos) {
            current_dir = current_dir.substr(0, pos);
        }

        full_path_to_FT_csv_file = config["ft_data_csv"].as<std::string>();
    
    } 

    CRT_RFT_UART RFT_SENSOR;

	initializeCSVFile(full_path_to_FT_csv_file);

    // Initialize and open the sensor port
    std::cout << "Initializing sensor..." << std::endl;
    if (!initializeSensor(RFT_SENSOR, devName, port, baudRate, byteSize)) {
        return -1;
    }
    std::cout << "Sensor initialized." << std::endl;



    // Set the desired data rate interval
    std::cout << "Setting data rate interval..." << std::endl;
    if (!setDataRate(RFT_SENSOR, dataRateInterval)) {
        return -1;
    }
    std::cout << "Data rate interval set." << std::endl;



    // Read and print FT data continuously
    std::cout << "Starting to read FT data..." << std::endl;
    readAndPrintFTData(full_path_to_FT_csv_file, RFT_SENSOR, dataRateInterval);


    // Close the sensor port (unreachable code in this example)
    RFT_SENSOR.rqst_FT_Stop();
    RFT_SENSOR.closePort();

    return 0;
}