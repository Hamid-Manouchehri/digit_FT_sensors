# set required version
cmake_minimum_required(VERSION 2.8)

# set project name
project(Powerball)

# set include drectories - this is the directory, from which cmake was started, i.e. the top level source directory
include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${CMAKE_SOURCE_DIR}/robotous_ft)



# set output paths
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")

set(ROBOTOUS_LIB_SRC
    src/RFT_IF_PACKET_REV.cpp
    src/RFT_UART_SAMPLE.cpp
)


# find_package(Boost COMPONENTS system signal thread REQUIRED)
add_library(robo_ft ${ROBOTOUS_LIB_SRC})
find_package(LSL REQUIRED)
find_package(yaml-cpp REQUIRED)


# compile executables
add_executable(ft_sensor src_main/FT_sensor.cpp)
target_link_libraries(ft_sensor pthread robo_ft)
target_link_libraries(ft_sensor yaml-cpp)

add_executable(lsl_ft src_main/LSL_FT.cpp)
target_link_libraries(lsl_ft pthread robo_ft LSL::lsl)
target_link_libraries(lsl_ft yaml-cpp)


