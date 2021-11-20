# -*- coding: utf-8 -*--v
import matplotlib
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
        
        self.mass_balance = {}

    def add_mass_balance_measurement(self, year, mass_balance, sub_measure):
        
        if year not in self.mass_balance:

            self.mass_balance[year] = mass_balance
        
        else:

            if sub_measure == True:
                self.mass_balance[year] += mass_balance
            
            else:
                self.mass_balance[year] += 0 


    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:

    def __init__(self, file_path):

        self.file_path = file_path
        self.glacier_collection = {}

        with open(self.file_path, newline = '') as f:
    
            file = csv.DictReader(f)

            for line in file:
                id = line[ "WGMS_ID" ]
                unit = line[ "POLITICAL_UNIT" ]
                name = line[ "NAME" ]
                lat  = float( line[ "LATITUDE" ] )
                lon  = float( line[ "LONGITUDE" ] )
                code = int( line[ "PRIM_CLASSIFIC" ] + line[ "FORM" ] + line[ "FRONTAL_CHARS" ] )
                self.glacier_collection[ id ] = Glacier( id, name, unit, lat, lon, code )
        


    def read_mass_balance_data(self, file_path):


        with open( file_path, newline = '') as f:
            file = csv.DictReader(f)

            for line in file:

                current_id = line[ "WGMS_ID" ] 
                current_year = line[ "YEAR" ]
                current_mass_balance = line[ "ANNUAL_BALANCE" ]
                current_lower_bound = line[ "LOWER_BOUND" ]
                
                if int( current_lower_bound ) != 9999:
                    sub_measure = True
                else:
                    sub_measure = False

                if  current_mass_balance== "": 
                    continue 
                else: 
                    self.glacier_collection[current_id].add_mass_balance_measurement(current_year, float(current_mass_balance), sub_measure)
                
       

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


file_path = Path("sheet-A.csv")
test = GlacierCollection(file_path)

test.read_mass_balance_data("sheet-EE.csv")
