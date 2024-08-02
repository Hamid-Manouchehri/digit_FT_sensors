#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <math.h>
#include <chrono>
#include <typeinfo> 
#include <fstream>
#include <vector>
#include <typeinfo>
#include <thread>
#include <mutex>
#include <condition_variable>
// #include <pthread.h>
#include <unistd.h>



// ft sensor header file
#include <memory.h>
#include "robotous_ft/RFT_UART_SAMPLE.h"
#include "robotous_ft/RFT_IF_PACKET_REV.h"

// Toon headers
// #include <TooN/TooN.h>
// #include <TooN/LU.h>
// #include <TooN/SVD.h>

// using namespace::TooN;

BYTE port = 1;

DWORD buad = B115200;

//DWORD buad = B921600;

DWORD byte_size = CS8;

CRT_RFT_UART RFT_SENSOR;

float		g_force_divider 	= 50.0f;			// for more information to refer the RFT sensor manual
float		g_torque_divider 	= 2000.0f;			// for more information to refer the RFT sensor manual



int main()
{
	bool isGo = true;

    
	char devName[] = "/dev/ttyUSB";
	RFT_SENSOR.openPort( devName, port, buad, byte_size );

	// initialize force/torque divider
	RFT_SENSOR.m_RFT_IF_PACKET.setDivider(g_force_divider, g_torque_divider); // V1.1
	usleep(1000);

	// RFT_SENSOR.rqst_FT_Continuous();
	RFT_SENSOR.set_FT_Bias(1);
	usleep(1000);


	std::ofstream datafile;

	// datafile.open("../data/01.csv");
	// datafile << "FT1,FT2,FT3,FT4,FT5,FT6" <<endl;


	while( isGo )
	{	

		
		// printf("here");
		// RFT_SENSOR.rqst_FT_Continuous();


		// datafile << FT[0] <<"," << FT[1] <<"," << FT[2]<< "," << FT[3] <<"," <<FT[4] <<"," << FT[5] << "," << "\n" ;
		char cmd = getchar();
		

		
		if( cmd == 0x1B ) // esc
			isGo = false;
		else if( cmd == 'M' || cmd == 'm' ) // measure
			RFT_SENSOR.rqst_FT_Continuous();
			// printf("hello;");

		else if( cmd == 'S' || cmd == 's' ) // stop
			RFT_SENSOR.rqst_FT_Stop();
		else if( cmd == 'B' || cmd == 'b' ) // bias
			RFT_SENSOR.set_FT_Bias(1);
		else if( cmd == 'U' || cmd == 'u' ) // un-bias
			RFT_SENSOR.set_FT_Bias(0);
		else
		{
			if( cmd != '\r' && cmd != '\n' )
				printf("UNKNOWN COMMAND\n");
		}

		// std::cout << FT[0] <<endl;

        
	}

	// std::cout << FT[0] <<endl;


	RFT_SENSOR.closePort();
	
	return 0;
}