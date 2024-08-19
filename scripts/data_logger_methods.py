#!/usr/bin/env python3

import csv

def setup_csv(file_path, file_name, fieldnames):
    """ Preparing csv data file in order to write data on it."""
    with open(file_path + file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)

def save_to_csv(file_path, file_name, data):
    with open(file_path + file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)