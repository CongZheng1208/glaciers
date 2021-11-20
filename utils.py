import csv
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """Return the distance in km between two points around the Earth.

    Latitude and longitude for each point are given in degrees.
    """
    R = 6371

    distance = 2 * R * math.asin( math.sqrt( math.sin((lat2 - lat1)/2) ** 2 + math.cos(lat1) * math.cos(lat2)* (math.sin((lon2 - lon1)/2)**2)) )

    return distance


def validation_for_id(id):

    if isinstance( id , int ):
        if len( str( id )) == 5:
            pass
        else:
            raise ValueError( "length of id should be 5" )
    else:
        raise TypeError( "id should be a integer" )
    
    return True

def validation_for_lat( lat ): 

    if lat > 90 or lat < -90 :
        raise ValueError(" latitude should be in range of (-90,90) ")
    else:
        pass

    return True

def validation_for_lon( lon ): 

    if lon > 180 or lon < -180:
        raise ValueError(" lontitude should be in range of (-180,180) ")
    else:
        pass

    return True

def validation_for_unit( unit ):

    if isinstance(unit, str):
        if len( unit ) != 2 :
            raise ValueError("length of unit should be 2")
        elif unit.isupper() or unit == "99": 
            pass
        else:
            raise ValueError("unit should be capital letters or 99")
    else:
        raise ValueError("unit should be a string")


    return True

def validation_for_year(year):

    if not isinstance( year, int ):
        raise ValueError(" year should be a integer ")
    elif year > 2021:
        raise ValueError(" year should be less than 2021 ")
    else: 
        pass

    return True


def validation_for_mass_balance( mass_balance ):

    if isinstance( mass_balance , int ):
        pass
    else:
        raise TypeError( "mass balance should be a integer" )
    
    return True


def validation_for_glaciers( id_collection, current_id ):
# 该函数用于检查EE数据集中的当前id是否存在于A数据集
    
    if current_id not in id_collection:
        raise ValueError(" The identifier of the glacier could not be recognized! It does not exist in the current glacier collection. ")
    else:
        pass

    return True
