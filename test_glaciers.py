import pytest
import utils

from glaciers import *
from pytest import raises


"""
The following test is used to test whether the add_mass_balance_measurement function
successfully reads the overall and partial measurement data.
"""

@pytest.mark.parametrize( 'glacier_id, desired_results',
                         [ ('04532', {'2015': -793.0, '2016': -418.0, '2017': 332.0, '2018': -7886.0, '2019': -2397.0, '2020': -13331.0}),
                           ('03903', {'2008': -537.0, '2009': -997.0, '2010': -1029.0, '2011': -2045.0, '2012': -1537.0, '2013': -823.0, '2014': -1359.0, '2015': -18969.0, '2016': 167.0, '2017': 798.0, '2018': -1511.0, '2019': -956.0}),
                           ('01675', {'1996': -460.0, '1997': 4460.0, '1998': -280.0, '2014': 206.0, '2015': -62.0, '2016': -8709.0, '2017': -22264.0, '2018': -8505.0, '2020': -535.0}),
                           ('03983', {'2004': -530.0, '2005': -1070.0, '2006': 210.0, '2007': -590.0, '2008': -210.0, '2009': -240.0, '2010': -770.0, '2011': -1000.0, '2012': -710.0, '2013': -510.0, '2014': -880.0, '2015': -1130.0}),
                         ] )                                           
def test_add_mass_balance_measurement( glacier_id, desired_results ):

    collection_for_code = GlacierCollection('sheet-A.csv')
    collection_for_code.read_mass_balance_data('sheet-EE.csv')

    assert collection_for_code.glacier_collection[glacier_id].mass_balance == desired_results


@pytest.mark.parametrize( 'year, mass_balance, sub_measure',
                         [ (2030, -100, True),
                           ('2030', 200, False)])
def test_add_mass_balance_measurement_failed_on_future_year( year, mass_balance, sub_measure ):
    with raises(ValueError) as e: 

        collection_for_code = Glacier('01234', 'GLACIER01', 'CN', -14.1, 23.1, '347')
        collection_for_code.add_mass_balance_measurement(year, mass_balance, sub_measure)

    exec_msg = e.value.args[0]
    assert exec_msg == "year should be earlier than 2021"
    

"""
The following test is used to test whether the filter_by_code function is 
suitable for complete code and non-complete code mode
"""

@pytest.mark.parametrize( 'code_pattern, desired_results',
                         [ ('628', ['CANITO', 'ADLER', 'RULUNG']),
                           ( 429 , ['EXPLORADORES', 'GROSSE', 'GUALAS N-TONGUE', 'GUALAS S-TONGUE', 'PARED SUR']),
                           ('1?8', [ ]),
                           ('32?', ['EIRIKSJOKULL', 'HOFSJOKUL_EYSTRI', 'HRUTFELL', 'ORAEFAJOKULL', 'SNAEFELLSJOKULL', 'THRANDARJOKULL', 'TINDFJALLAJOKULL', 'TORFAJOKULL', 'TUNGNAFELLSJOKULL']),
                           ('1??', ['TORRE']),
                           ('?6?', [ ]) ] )
def test_filter_by_code( code_pattern, desired_results ):

    collection_for_code = GlacierCollection('sheet-A.csv')
    collection_for_code.read_mass_balance_data('sheet-EE.csv')

    assert collection_for_code.filter_by_code(code_pattern) == desired_results



@pytest.mark.parametrize( 'code_pattern',
                         [ '12x',
                           '3?a',
                           '1D2'])
def test_filter_by_code_failed_on_non_permitted_format( code_pattern ):
    with raises(ValueError) as e: 

        collection_for_code = GlacierCollection('sheet-A.csv')
        collection_for_code.read_mass_balance_data('sheet-EE.csv')
        collection_for_code.filter_by_code(code_pattern)

    exec_msg = e.value.args[0]
    assert exec_msg == "Code pattern must contain only digits and ?"


@pytest.mark.parametrize( 'code_pattern',
                         [ '4628',
                           '3???',
                           '12'])
def test_filter_by_code_fail_on_non_3_length_code_pattern( code_pattern ):
    with raises(ValueError) as e: 

        collection_for_code = GlacierCollection('sheet-A.csv')
        collection_for_code.read_mass_balance_data('sheet-EE.csv')
        collection_for_code.filter_by_code(code_pattern)

    exec_msg = e.value.args[0]
    assert exec_msg == "length of code pattern should be 3"


@pytest.mark.parametrize( 'code_pattern',
                         [  3.452,
                            {'key', 378},
                            ['29?']])
def test_filter_by_code_fail_on_non_permitted_type( code_pattern ):
    with raises(TypeError) as e: 

        collection_for_code = GlacierCollection('sheet-A.csv')
        collection_for_code.read_mass_balance_data('sheet-EE.csv')
        collection_for_code.filter_by_code(code_pattern)

    exec_msg = e.value.args[0]
    assert exec_msg == "code pattern should be a integer or a string"


"""
The following test is used to test whether the sort_by_latest_mass_balance function 
can be applied to sorting in different directions.
"""

@pytest.mark.parametrize( 'n, reverse, desired_results',
                         [ ( 5 , False, ['CHHOTA SHIGRI', 'REMBESDALSKAAKA', 'BLAAISEN', 'CAINHAVARRE', 'STORSTEINSFJELLBREEN']),
                           ( 4 , False, ['REMBESDALSKAAKA', 'BLAAISEN', 'CAINHAVARRE', 'STORSTEINSFJELLBREEN']),
                           ( 10, False, ['BATAL', 'DYNGJUJOKULL', 'BAEGISARJOKULL', 'MIDTRE FOLGEFONNA', 'SIDUJOKULL E M 177', 'CHHOTA SHIGRI', 'REMBESDALSKAAKA', 'BLAAISEN', 'CAINHAVARRE', 'STORSTEINSFJELLBREEN']),
                           ( 5 , True, ['ARTESONRAJU', 'TUNSBERGDALSBREEN', 'PARLUNG NO. 94', 'GRAAFJELLSBREA', 'AGUA NEGRA']),
                           ( 3 , True, ['ARTESONRAJU', 'TUNSBERGDALSBREEN', 'PARLUNG NO. 94']),
                           ( 6 , True, ['ARTESONRAJU', 'TUNSBERGDALSBREEN', 'PARLUNG NO. 94', 'GRAAFJELLSBREA', 'AGUA NEGRA', 'MIDTDALSBREEN']) ] )
def test_sort_by_latest_mass_balance( n, reverse, desired_results ):

    collection_for_code = GlacierCollection('sheet-A.csv')
    collection_for_code.read_mass_balance_data('sheet-EE.csv')
    collection_sorted = collection_for_code.sort_by_latest_mass_balance( n, reverse )

    list_sorted_name = []

    for i in range(len(collection_sorted)):
        list_sorted_name.append(collection_sorted[i].name)

    assert  list_sorted_name == desired_results


@pytest.mark.parametrize( 'n, reverse',
                         [ (-5, False),
                           (0,  False) ])
def test_sort_by_latest_mass_balance_fail_on_non_permitted_n( n, reverse ):
    with raises(ValueError) as e: 

        collection_for_code = GlacierCollection('sheet-A.csv')
        collection_for_code.read_mass_balance_data('sheet-EE.csv')
        collection_for_code.sort_by_latest_mass_balance( n, reverse )

    exec_msg = e.value.args[0]
    assert exec_msg == "n should be an integer more than 0"


@pytest.mark.parametrize( 'n, reverse',
                         [ ('5', False),
                           ([5],  False) ])
def test_sort_by_latest_mass_balance_failed_on_non_permitted_n_type( n, reverse ):
    with raises(TypeError) as e: 

        collection_for_code = GlacierCollection('sheet-A.csv')
        collection_for_code.read_mass_balance_data('sheet-EE.csv')
        collection_for_code.sort_by_latest_mass_balance( n, reverse )

    exec_msg = e.value.args[0]
    assert exec_msg == "n should be a integer"


"""The following test is used to test whether proper data input will proceed smoothly."""

@pytest.mark.parametrize( 'csv',
                         ['sheet-A.csv',
                          'sheet-EE.csv',
                          'congzheng.csv'])
def test_validation_for_csv( csv ):
    assert utils.validation_for_csv( csv )


@pytest.mark.parametrize( 'id',
                         ['12345',
                          '89201',
                          '04320'])
def test_validation_for_id( id ):
    assert utils.validation_for_id( id )


@pytest.mark.parametrize( 'lat',
                         [ 12,
                           -35,
                           17.43 ])
def test_validation_for_lat( lat ):
    assert utils.validation_for_lat( lat )


@pytest.mark.parametrize( 'lon',
                         [ 12,
                          -70,
                          0.31])
def test_validation_for_lon( lon ):
    assert utils.validation_for_lon( lon )


@pytest.mark.parametrize( 'unit',
                         ['SA',
                          'TZ',
                          '99'])
def test_validation_for_unit( unit ):
    assert utils.validation_for_unit( unit )


@pytest.mark.parametrize( 'year',
                         ['1972',
                          '2008',
                          '2020'])
def test_validation_for_year( year ):
    assert utils.validation_for_year( year )


@pytest.mark.parametrize( 'mass_balance',
                         [ 200,
                           -1300,
                           3590.43])
def test_validation_for_mass_balance( mass_balance ):
    assert utils.validation_for_mass_balance( mass_balance )


@pytest.mark.parametrize( 'code_pattern',
                         ['259',
                          '321',
                          '000' ])
def test_validation_for_code_pattern_full_code( code_pattern ):
    assert utils.validation_for_code_pattern( code_pattern ) == True

@pytest.mark.parametrize( 'code_pattern',
                         ['3??',
                          '4?6',
                          '?12'])
def test_validation_for_code_pattern_non_full_code( code_pattern ):
    assert utils.validation_for_code_pattern( code_pattern ) == False


@pytest.mark.parametrize( 'n',
                         [ 5,
                           200,
                           10000])
def test_validation_for_n( n ):
    assert utils.validation_for_n( n )


"""The following test is used to test whether improper data input will report the corresponding error."""

@pytest.mark.parametrize( 'csv',
                         [ 'sheet-A.txt',
                           'sheet-A.excl',
                           'sheet-EE.mp4'])
def test_validation_for_csv_fail_on_non_permitted_file_type( csv ):
    with raises(IOError) as e: 
        utils.validation_for_csv( csv )

    exec_msg = e.value.args[0]
    assert exec_msg == "please input a csv file"


def test_validation_for_id_fail_on_non_5_length_id():
    with raises(ValueError) as e: 
        utils.validation_for_id( '782012' )

    exec_msg = e.value.args[0]
    assert exec_msg == "length of id should be 5"


def test_validation_for_id_fail_on_non_numeric_id():
    with raises(ValueError) as e: 
        utils.validation_for_id( '78UX1' )

    exec_msg = e.value.args[0]
    assert exec_msg == "id should all consist of numbers"


def test_validation_for_lat_fail_on_non_permitted_lat():
    with raises(ValueError) as e: 
        utils.validation_for_lat( 120 )

    exec_msg = e.value.args[0]
    assert exec_msg == "latitude should be in range of (-90,90)"


def test_validation_for_unit_fail_on_non_permitted_unit():
    with raises(ValueError) as e: 
        utils.validation_for_unit( 'Zy' )

    exec_msg = e.value.args[0]
    assert exec_msg == "unit should be capital letters or 99"


def test_validation_for_year_fail_on_future_year():
    with raises(ValueError) as e: 
        utils.validation_for_year( '2035' )

    exec_msg = e.value.args[0]
    assert exec_msg == "year should be earlier than 2021"


def test_validation_for_code_pattern_fail_on_non_3_length_code():
    with raises(ValueError) as e: 
        utils.validation_for_code_pattern( '32??3' )

    exec_msg = e.value.args[0]
    assert exec_msg == "length of code pattern should be 3"


def test_validation_for_code_pattern_fail_on_non_permitted_code():
    with raises(ValueError) as e: 
        utils.validation_for_code_pattern( '4#?' )

    exec_msg = e.value.args[0]
    assert exec_msg == "Code pattern must contain only digits and ?"


def test_validation_for_code_pattern_fail_on_non_permitted_type():
    with raises(TypeError) as e: 
        utils.validation_for_code_pattern( ['4#2'] )

    exec_msg = e.value.args[0]
    assert exec_msg == "code pattern should be a integer or a string"
