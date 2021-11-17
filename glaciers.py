# -*- coding: utf-8 -*--v
import matplotlib
import pytest
import csv
from pathlib import Path


class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):

        self.glacier_id = glacier_id
        self.name = name
        self.unit = unit
        self.lat = lat
        self.lon = lon
        self.code = code
        
        self.mass_balance = []
        
        #raise NotImplementedError

    def add_mass_balance_measurement(self, year, mass_balance):
        raise NotImplementedError

    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:

    def __init__(self, file_path):

        self.file_path = file_path
        self.glacier_collection = []

        with file_path.open() as f:
    
            file = csv.DictReader(f)

            for line in file:
                #print(line[0])
                print(line[1])
                print(line[2])



    def read_mass_balance_data(self, file_path):
        raise NotImplementedError

    def find_nearest(self, lat, lon, n):
        """Get the n glaciers closest to the given coordinates."""
        raise NotImplementedError
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        raise NotImplementedError

    def sort_by_latest_mass_balance(self, n, reverse):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        raise NotImplementedError

    def summary(self):
        raise NotImplementedError

    def plot_extremes(self, output_path):
        raise NotImplementedError


file_path = Path("/Users/congzheng/Desktop/sheet-A.csv")
collection = GlacierCollection(file_path)


#with open(file_path, newline = '') as f:
    
#    file = csv.reader(f)

#   for line in file:
#        print(line[3])

