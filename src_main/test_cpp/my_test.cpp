#include <fstream>
#include <iostream>
#include <cstdlib>
#include <stdio.h>

#include <string>
#include <chrono>
#include <iomanip>
#include <sstream>

using namespace std;


// Function to get the current time as a string in ISO 8601 format
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


void recordDataWithTimestamp(const std::string& directory, const std::string& baseFileName, int numberOfFiles, const std::string& csvFilePath) {
    std::string fileExtension = ".txt";
    
    // Open the CSV file in append mode
    std::ofstream datafile;
    datafile.open(csvFilePath, std::ios::app);

    if (!datafile.is_open()) {
        std::cerr << "Error opening file: " << csvFilePath << std::endl;
        return;
    }

    for (int i = 1; i <= numberOfFiles; ++i) {
        // Create a new file name by appending the loop index
        std::string fileName = baseFileName + std::to_string(i) + fileExtension;

        // Concatenate the directory and file name to get the full path
        std::string fullPath = directory + fileName;

        // Get the current time in ISO 8601 format
        std::string currentTime = getCurrentTimeISO8601();

        // Output the full path and current time to the CSV file
        datafile << fullPath << "," << currentTime << "\n";
    }

    datafile.close();
}


int main()
{

    // int numbers[6] = {1, 2, 3, 4, 5, 6};

    // string directory = "/data/users/hmanouch/projects/CMAKE_FT_TEST/src_main/csv_data/";
    // string fileName = "FT_sensor_data_1.csv";

    // // Concatenate the directory and file name
    // string fullPath = directory + fileName;

    // ofstream datafile;
    // datafile.open(fullPath);
    // datafile << "FT1,FT2,FT3,FT4,FT5,FT6\n";

    // datafile << numbers[0] << "," << numbers[1] << "," << numbers[2] << ","
    //             << numbers[3] << "," << numbers[4] << "," << numbers[5] << "\n";




    // string directory = "/data/users/hmanouch/projects/DIGIT/digit_tactile_sensor/";
    // string fileName = "take_digit_image.py";
    // string fullPath = directory + fileName;
    // string command = "python3 " + fullPath + " name2";

    // int result = std::system(command.c_str());



    // cout << std::to_string(12) << "\n";




    std::string directory = "/path/to/directory/";
    std::string baseFileName = "file_";
    int numberOfFiles = 5;
    std::string csvFilePath = "file_paths_with_timestamps.csv";

    // Call the function to generate file paths and append to CSV file
    recordDataWithTimestamp(directory, baseFileName, numberOfFiles, csvFilePath);



    return 0;
}
