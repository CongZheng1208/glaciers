# -*- coding: utf-8 -*--v
from pathlib import Path
import math


def haversine_distance( lat1, lon1, lat2, lon2 ):
    """
    Return the distance in km between two points around the Earth.
    Latitude and longitude for each point are given in degrees.
    """

    validation_for_lat( lat1 )
    validation_for_lat( lat2 )
    validation_for_lon( lon1 )
    validation_for_lon( lon2 )

    R = 6371

    distance =  2 * R * math.asin( math.sqrt( math.sin( ( lat2 - lat1 ) / 2 ) **2 + ( ( math.cos( lat1 ) * math.cos( lat2 ) ) * ( math.sin( ( lon2-lon1 ) / 2 ) **2 ) ) ))
    return distance


def validation_for_csv( file_path ):
    """This function is used to verify the correctness of the input file format"""

    file_path = str( file_path )

    if file_path.split( "." )[ -1 ] != 'csv':

        raise IOError( "please input a csv file" )

    else:

        pass
    
    return True


def validation_for_id(id):
    """This function is used to verify the correctness of the glacier identifier"""

    if isinstance( id, str ):

        if id.isdigit( ):

            if len( id ) == 5:
                pass
            else:
                raise ValueError( "length of id should be 5" )
        
        else:

            raise ValueError( "id should all consist of numbers" ) 
            

    else:

        raise TypeError( "id should be a string constructed from numbers" )

 
    
    return True


def validation_for_lat( lat ): 
    """This function is used to verify the correctness of the latitude"""

    if isinstance( lat , float ) or isinstance( lat, int ):
        if lat > 90 or lat < -90 :

            raise ValueError("latitude should be in range of (-90,90)")

        else:

            pass
    else:

        raise TypeError("latitude should be a number")

    return True


def validation_for_lon( lon ): 
    """This function is used to verify the correctness of longitude"""

    if isinstance( lon , float ) or isinstance( lon, int ):

        if lon > 180 or lon < -180:

            raise ValueError("lontitude should be in range of (-180,180)")

        else:

            pass
    else:

        raise TypeError("lontitude should be a number")

    return True


def validation_for_unit( unit ):
    """This function is used to verify the correctness of the political unit"""

    if isinstance(unit, str):

        if len( unit ) != 2 :
            raise ValueError("length of unit should be 2")
        elif unit.isupper() or unit == "99": 
            pass
        else:
            raise ValueError("unit should be capital letters or 99")

    else:

        raise TypeError("unit should be a string")

    return True


def validation_for_year(year):
    """This function is used to verify the correctness of the year"""

    if isinstance( year, str ):

        if not year.isdigit():

            raise ValueError("year should be constructed from numbers")

        elif int(year) > 2021:

            raise ValueError("year should be earlier than 2021")

        else:

            pass

    elif isinstance( year, int ):

        if year > 2021:

            raise ValueError("year should be earlier than 2021")

        else:

            pass
    
    else:

        raise TypeError("year should be a integer or a string constructed from numbers")

    return True


def validation_for_mass_balance( mass_balance ):
    """This function is used to verify the correctness of the mass balance measurement"""

    if isinstance( mass_balance, int) or isinstance( mass_balance, float) :

        pass

    else:

        raise TypeError( "mass balance should be a integer" )
    
    return True


def validation_for_code_pattern( code_pattern ):
    """This function is used to verify the correctness of the code pattern"""

    if isinstance( code_pattern , str ):

        if len( code_pattern ) == 3:

            if all( (char.isdigit() or char =='?') for char in code_pattern):

                if all((char == "?") for char in code_pattern):

                    raise ValueError("Need atleast one digit in code pattern")
                 
                elif all(char.isdigit() for char in code_pattern):

                    full_code = True 

                else: 

                    full_code = False

            else: 
                raise ValueError("Code pattern must contain only digits and ?")
        
        else:
            raise ValueError( "length of code pattern should be 3" )


    elif isinstance(code_pattern, int):

        if len( str( code_pattern )) == 3:

            full_code = True
        
        else:
        
            raise ValueError( "length of code pattern should be 3" )
    
    else:
        
        raise TypeError( "code pattern should be a integer or a string" )
    
    return full_code


def validation_for_n( n ): 
    """This function is used to verify n"""

    if isinstance( n , int ):

        if n <= 0:

            raise ValueError( "n should be an integer more than 0" )

        else:

            pass
    else:

        raise TypeError( "n should be a integer" )

    return True


def validation_for_reverse( reverse ): 
    """This function is used to verify reverse"""

    if isinstance( reverse , bool ):
        
        pass
    
    else:

        raise TypeError( "reverse should be a boolean" )

    return True


def validation_for_glaciers( id_collection, current_id ):
    """This function is used to check whether the current id in the EE data set exists in the A data set"""
    
    if current_id not in id_collection:

        raise ValueError("The identifier of the glacier could not be recognized! It does not exist in the current glacier collection.")

    else:

        pass

    return True
