#!/usr/bin/env python3

import csv

def setup_csv(file_path, fieldnames):
    """ Preparing csv data file in order to write data on it."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)

def save_to_csv(data, file_path):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)