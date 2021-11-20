# -*- coding: utf-8 -*--v

import csv
import sys
import utils

from pathlib import Path
from matplotlib import pyplot

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

            self.mass_balance[ year ] = mass_balance
        
        else:

            if sub_measure == True:
                self.mass_balance[ year ] += mass_balance
            
            else:
                self.mass_balance[ year ] += 0 


    def plot_mass_balance(self, output_path):

        x_values = []
        y_values = []

        # make sure that the glacier has mass balance measurements
        if self.mass_balance: 

            for year in self.mass_balance.keys():

                x_values.append( year )
                y_values.append( self.mass_balance[year] )
        
            pyplot.pyplot.figure()
            pyplot.plot(x_values, y_values)

            pyplot.xlabel( "Year" )
            pyplot.ylabel( "Mass Balance [mm.w.e]" )
    
            pyplot.title( str( self.name ) + "Mass Balance Measurements Vs Years")
            pyplot.savefig( output_path + str( self.name ) + "_mass_balance_plot.png")
        
        else:

            print("This glacier has no record of mass balance.")


    def get_id(self):
        return self.glacier_id

    def get_code(self):
        return self.code

    def get_latitude(self):
        return self.lat

    def get_lontitude(self):
        return self.lon

    def get_name(self):
        return self.name

    def get_mass(self):
        return self.mass_balance

        
class GlacierCollection:

    def __init__(self, file_path):

        self.file_path = file_path

        utils.validation_for_csv(file_path)

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

                #utils.validation_for_id( id )
                utils.validation_for_unit( unit )
                utils.validation_for_lat( lat )
                utils.validation_for_lon( lon )

                self.glacier_collection[ id ] = Glacier( id, name, unit, lat, lon, code )
        


    def read_mass_balance_data(self, file_path):

        utils.validation_for_csv( file_path )

        with open( file_path, newline = '') as f:

            file = csv.DictReader(f)            

            id_collection = self.glacier_collection.keys()

            for line in file:

                current_id = line[ "WGMS_ID" ] 
                current_year = line[ "YEAR" ]
                current_mass_balance = line[ "ANNUAL_BALANCE" ]
                current_lower_bound = line[ "LOWER_BOUND" ]
                
                utils.validation_for_glaciers(id_collection, current_id)
                
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
        # print the number of glaciers in collection
        print("This collection has", len(self.glacier_collection), "glaciers")

        # tracking variables 
        earliest_year = sys.maxsize
        glacier_w_measure = 0 
        shrink = 0 
        grow = 0 

        for glacier in self.glacier_collection:

            glac = self.glacier_collection[glacier]

            # find the earliest measurement
            year_order = sorted(glac.mass_balance.keys(), key=lambda key: key)

            if len(year_order) != 0:
                year  = int(year_order[0]) 
                if int(year) <= earliest_year:
                    earliest_year = year

                # find out if the last measurement saw the glacier shrink
                latest_year = year_order[-1]
                mass_measurement = glac.mass_balance[latest_year]
                if mass_measurement < 0: 
                    shrink += 1
                else: 
                    grow += 1
                
                glacier_w_measure += 1
            else: 
                continue
        
        shrink_perc = int( round( 100 * shrink / glacier_w_measure ))
        print( "The earliest measurement was in", earliest_year )
        print( str( shrink_perc ) + "% of glaciers shrunk in their last measurement" )


    def plot_extremes(self, output_path):
        # tracking variables
        most_shrink = sys.maxsize
        shrink_id = None
        most_grow = -sys.maxsize
        grow_id = None

        for glacier in self.glacier_collection.values():
            #glac = self.glacier_collection[glacier]
            
            #sort the years from oldest to most recent
            year_order = sorted(glacier.mass_balance.keys(), key=lambda key: key)
            
            if len(year_order) != 0: # making sure the glacier has some measurements
                latest_year = year_order[-1]
                mass_measure = glacier.mass_balance[latest_year]
                
                if mass_measure < 0 and mass_measure < most_shrink:
                    most_shrink = mass_measure
                    shrink_id = glacier.glacier_id
                
                elif mass_measure > 0 and mass_measure > most_grow:
                    most_grow = mass_measure
                    grow_id = glacier.glacier_id

            

        x_values_0 = []
        y_values_0 = []
        # make sure that the glacier has mass balance measurements
        for year in self.glacier_collection[shrink_id].mass_balance:
            x_values_0.append(int(year))
            y_values_0.append(self.glacier_collection[shrink_id].mass_balance[year])

        # plotting
        pyplot.figure()
        pyplot.plot(x_values_0, y_values_0)
        pyplot.xlabel("Year")
        pyplot.ylabel("Mass Balance [mm.w.e]")
        pyplot.title("Glacier Collection Shrink Plot")

        pyplot.savefig(output_path+"extremes_plot0.png")

        x_values_1 = []
        y_values_1 = []
        # make sure that the glacier has mass balance measurements
        for year in self.glacier_collection[grow_id].mass_balance:
            x_values_1.append(int(year))
            y_values_1.append(self.glacier_collection[grow_id].mass_balance[year])

        # plotting
        pyplot.figure()
        pyplot.plot(x_values_1, y_values_1)
        pyplot.xlabel("Year")
        pyplot.ylabel("Mass Balance [mm.w.e]")
        pyplot.title("Glacier Collection Grow Plot")

        pyplot.savefig(output_path+"extremes_plot1.png")


file_path = Path("sheet-A.csv")
test = GlacierCollection(file_path)
test.read_mass_balance_data("sheet-EE.csv")
test.summary()
test.plot_extremes("/Users/congzheng/Desktop/")