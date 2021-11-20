from glaciers import *
from pytest import raises

def main():
    file_path = Path("sheet-A.csv")
    test = GlacierCollection(file_path)
    test.read_mass_balance_data("sheet-EE.csv")
    test.summary()
    #print(test.glacier_collection.keys())
    test.plot_extremes("/Users/congzheng/Desktop/")
    list1 = test.sort_by_latest_mass_balance( n=5, reverse = True )

    for i in range(5):
        print( list1[i].get_glacier_id() )

    names = test.filter_by_code('4?3')

    for i in range(len(names)):
        print( names[i])

def test_filter():
    file_path = Path("sheet-A.csv")
    collection = GlacierCollection(file_path)
    file_path_2=Path("sheet-EE.csv")
    collection.read_mass_balance_data(file_path_2)
    filter_collection=collection.filter_by_code('638')
    print(*filter_collection)
    filter_collection_2=collection.filter_by_code('6?8')

def test_validation_for_glacier_fail_on_non_5_length_id():
      with raises(ValueError) as exception: 
          validation_for_glacier('1444',0,0,0)
    
def test_validation_for_glacier_fail_on_non_valid_latitude():
      with raises(ValueError) as exception: 
         validation_for_glacier('14444',-190,0,0)
def test_validation_for_glacier_fail_on_non_number_id():
    with raises(TypeError) as exception:
         validation_for_glacier('jimmy',0,0,0)
def test_validation_for_glacier_fail_on_non_valid_unit():
    with raises(ValueError) as exception:
         validation_for_glacier('14444',0,0,'aed')
    