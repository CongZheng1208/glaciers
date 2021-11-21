import pytest
import utils

from glaciers import *
from pytest import raises



"""以下测试用于测试适当的数据输入是否会顺利进行"""

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


"""以下测试用于测试不当的数据输入是否会报出相应的错误"""

def test_validation_for_csv_fail_on_non_permitted_file_type():
    with raises(IOError) as e: 
        utils.validation_for_csv( 'sheet-A.txt' )

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


"""以下测试用于测试add_mass_balance_measurement函数是否顺利读取了整体和局部测量的数据"""


   
    

"""以下测试用于测试filter_by_code函数是否适用于完整代码和非完整代码模式"""


"""以下测试用于测试sort_by_latest_mass_balance函数是否能够适用于不同方向的排序"""
