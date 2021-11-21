# -*- coding: utf-8 -*--v

import csv
import re
import sys
import utils

from pathlib import Path
from matplotlib import pyplot

class Glacier:

    def __init__(self, glacier_id, name, unit, lat, lon, code):
        """This function is used to initialize the glacier object"""

        self.__glacier_id = glacier_id
        self.__name = name
        self.__unit = unit
        self.__lat = lat
        self.__lon = lon
        self.__code = code
        self.__mass_balance = {}

    def add_mass_balance_measurement(self, year, mass_balance, sub_measure):
        """This function is used to add its mass balance value to the glacier objec"""

        utils.validation_for_year( year )
        utils.validation_for_mass_balance( mass_balance )
        
        if year not in self.__mass_balance:

            self.__mass_balance[ year ] = mass_balance
        
        else:

            if sub_measure == True:

                self.__mass_balance[ year ] += mass_balance
            
            else:

                self.__mass_balance[ year ] += 0 


    def plot_mass_balance(self, output_path):
        """This function is used to draw the change trend of the mass balance value of the glacier object"""

        x_values = []
        y_values = []

        if self.__mass_balance: 

            for year in self.__mass_balance.keys():

                x_values.append( year )
                y_values.append( self.__mass_balance[ year ] )
        
            pyplot.figure()
            pyplot.plot( x_values, y_values )
            pyplot.xlabel( "Year" )
            pyplot.ylabel( "Mass Balance Measurement [mm.w.e]" )
            pyplot.title( str( self.__name ) + "'s diagram of changes in mass balance")
            pyplot.savefig( output_path + str( self.__name ) + "'s diagram of changes in mass balance.png")
        
        else:

            print("This glacier has no record of mass balance.")


    def get_glacier_id(self):
        """This function is used to obtain the identifier of the glacier object"""

        return self.__glacier_id


    def get_name(self):
        """This function is used to get the name of the glacier object"""

        return self.__name


    def get_unit(self):
        """This function is used to obtain the unit of the glacier object"""

        return self.__unit


    def get_latitude(self):
        """This function is used to get the latitude of the glacier object"""

        return self.__lat


    def get_lontitude(self):
        """This function is used to obtain the longitude of the glacier object"""

        return self.__lon
    

    def get_code(self):
        """This function is used to obtain the code of the glacier object"""

        return self.__code


    def get_mass_balance(self):
        """This function is used to obtain the mass balance measurement of the glacier object"""

        return self.__mass_balance

        
class GlacierCollection:

    def __init__(self, file_path):
        """This function is used to initialize the glacier object collection"""

        utils.validation_for_csv( file_path )

        self.file_path = file_path
        self.glacier_collection = {}

        with open(self.file_path, newline = '') as file:
    
            dict_file = csv.DictReader(file)

            for line in dict_file:

                id = line[ "WGMS_ID" ]
                unit = line[ "POLITICAL_UNIT" ]
                name = line[ "NAME" ]
                lat  = float( line[ "LATITUDE" ] )
                lon  = float( line[ "LONGITUDE" ] )
                code = int( line[ "PRIM_CLASSIFIC" ] + line[ "FORM" ] + line[ "FRONTAL_CHARS" ] )

                utils.validation_for_id( id )
                utils.validation_for_unit( unit )
                utils.validation_for_lat( lat )
                utils.validation_for_lon( lon )

                self.glacier_collection[ id ] = Glacier( id, name, unit, lat, lon, code )
        


    def read_mass_balance_data(self, file_path):
        """This function is used to read the mass balance measurement of the glacier object collection and add it to the corresponding glacier object"""

        utils.validation_for_csv( file_path )

        with open( file_path, newline = '') as file:

            dict_file = csv.DictReader(file)            

            id_collection = self.glacier_collection.keys()

            for line in dict_file:

                current_id = line[ "WGMS_ID" ] 
                current_year = line[ "YEAR" ]
                current_mass_balance = line[ "ANNUAL_BALANCE" ]
                current_lower_bound = line[ "LOWER_BOUND" ]
                
                utils.validation_for_glaciers( id_collection, current_id )
                
                if int( current_lower_bound ) != 9999:

                    sub_measure = True

                else:

                    sub_measure = False

                if  current_mass_balance== "": 

                    continue 

                else: 

                    self.glacier_collection[ current_id ].add_mass_balance_measurement( current_year, float( current_mass_balance ), sub_measure )
       

    def find_nearest( self, lat, lon, n = 5 ):
        """Get the n glaciers closest to the given coordinates."""

        utils.validation_for_lat( lat )
        utils.validation_for_lon( lon )
        utils.validation_for_n( n )

        distance_collection = {} 

        for current_glacier in self.glacier_collection.values():

            lat2, lon2 = current_glacier.get_latitude(), current_glacier.get_lontitude()
            distance = utils.haversine_distance( lat, lon, lat2, lon2 )
            distance_collection[ current_glacier.get_name() ] = distance
        
        distance_collection = dict( sorted( distance_collection.items(), key=lambda item: item[1] ) )
        names = list( distance_collection.keys() )[ :n ]

        return names
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""

        full_code = utils.validation_for_code_pattern( code_pattern )
        glacier_names = []
    
        if full_code:

            for key in self.glacier_collection:
                if self.glacier_collection[ key ].get_code() == code_pattern:          
                    glacier_names.append( self.glacier_collection[ key ].get_name() )
        
        else: 

            match_data = []
            match_regular_expression = re.compile( r"\d" )
            for match_item in match_regular_expression.finditer( code_pattern ):
                match_data.append( match_item.start() )
        
            if len(match_data) == 1:
                index_0 = match_data[ 0 ]
                for match_key in self.glacier_collection.keys():

                    if str(self.glacier_collection[ match_key ].get_code() )[ index_0 ] == code_pattern[ index_0 ]:
                        glacier_names.append( self.glacier_collection[ match_key ].get_name() )
        
            elif len(match_data) == 2:
                index_0, index_1 = match_data[ 0 ], match_data[ 1 ] 
                for match_key in self.glacier_collection:

                    glacier_match_code = str( self.glacier_collection[ match_key ].get_code() )
                    if glacier_match_code[ index_0 ] == code_pattern[ index_0 ] and glacier_match_code[ index_1 ] == code_pattern[ index_1 ]:
                        glacier_names.append( self.glacier_collection[ match_key ].get_name() )
     
        return glacier_names


    def sort_by_latest_mass_balance( self, n = 5, reverse = False ):
        """Return the N glaciers with the highest area accumulated in the last measurement."""

        utils.validation_for_n(n)

        mass_balance_collection = {}
        latest_mass_balance_collection = []
    
        for current_glacier in self.glacier_collection.values():
            
            current_year_order = sorted( current_glacier.get_mass_balance().keys(), key=lambda key: key )
            
            if len(current_year_order) != 0: 

                latest_year = current_year_order[ -1 ]
                mass_balance_collection[ current_glacier.get_glacier_id() ] = current_glacier.get_mass_balance()[ latest_year ]
            
            else:

                continue

        mass_balance_collection = dict( sorted( mass_balance_collection.items(), key=lambda item: item[1] ))
        keys = list( mass_balance_collection.keys() )

        if reverse == False:

            keys = keys[ -n: ]
            for key in keys: 
                latest_mass_balance_collection.append( self.glacier_collection[ key ] ) 

        else: 

            keys = keys[ :n ]
            for key in keys:
                latest_mass_balance_collection.append( self.glacier_collection[ key ] )

        return latest_mass_balance_collection

    def summary(self):
        """
        This function is used to print the total number of glaciers in the glacier object collection, 
        the earliest measurement year, and the proportion of glaciers whose mass balance decreases.
        """

        print( "This collection has", len( self.glacier_collection ), "glaciers" )

        earliest_year = sys.maxsize

        glacier_measure_count = 0 
        shrink_count = 0 
        grow_count = 0 

        for current_glacier in self.glacier_collection.values():

            year_order = sorted(current_glacier.get_mass_balance().keys(), key=lambda key: key)

            if len(year_order) != 0:

                year  = int(year_order[0]) 

                if int(year) <= earliest_year:
                    earliest_year = year

                latest_year = year_order[-1]
                mass_measurement = current_glacier.get_mass_balance()[latest_year]

                if mass_measurement < 0: 
                    shrink_count += 1
                else: 
                    grow_count += 1
                
                glacier_measure_count += 1
            else: 
                continue
        
        shrink_percent = int( round( 100 * shrink_count / glacier_measure_count ))
        print( "The earliest measurement was in", earliest_year )
        print( str( shrink_percent ) + "% of glaciers shrunk in their last measurement" )


    def plot_extremes(self, output_path):
        """
        This function is used to draw the historical mass balance measurement of the glacier object with 
        the largest and smallest changes in the recent period.
        """
     
        most_shrink = sys.maxsize
        shrink_id = None
        most_grow = -sys.maxsize
        grow_id = None

        for current_glacier in self.glacier_collection.values():
            
            year_order = sorted(current_glacier.get_mass_balance().keys(), key=lambda key: key)
            
            if len(year_order) != 0: 
                latest_year = year_order[-1]
                mass_measure = current_glacier.get_mass_balance()[latest_year]
                
                if mass_measure < 0 and mass_measure < most_shrink:
                    most_shrink = mass_measure
                    shrink_id = current_glacier.get_glacier_id()
                
                elif mass_measure > 0 and mass_measure > most_grow:
                    most_grow = mass_measure
                    grow_id = current_glacier.get_glacier_id()
         
        x_values_0 = []
        y_values_0 = []

        for year in self.glacier_collection[shrink_id].get_mass_balance():
            x_values_0.append(int(year))
            y_values_0.append(self.glacier_collection[shrink_id].get_mass_balance()[year])

        pyplot.figure()
        pyplot.plot(x_values_0, y_values_0)
        pyplot.xlabel("Year")
        pyplot.ylabel("Mass Balance Measurement [mm.w.e]")
        pyplot.title("Diagram of the glaciers with the most growth in mass balance")

        pyplot.savefig( output_path + "Diagram of the glaciers with the most growth in mass balance.png" )

        x_values_1 = []
        y_values_1 = []

        for year in self.glacier_collection[grow_id].get_mass_balance():
            x_values_1.append(int(year))
            y_values_1.append(self.glacier_collection[grow_id].get_mass_balance()[year])

        pyplot.figure()
        pyplot.plot( x_values_1, y_values_1 )
        pyplot.xlabel("Year")
        pyplot.ylabel("Mass Balance Measurement [mm.w.e]")
        pyplot.title("Diagram of the glaciers with the most shrinking mass balance")

        pyplot.savefig( output_path + "Diagram of the glaciers with the most shrinking mass balance.png" )


file_path = Path("sheet-A.csv")
test = GlacierCollection(file_path)
test.read_mass_balance_data("sheet-EE.csv")
test.summary()
#print(test.filter_by_code('??6'))
print(test.sort_by_latest_mass_balance(  ))