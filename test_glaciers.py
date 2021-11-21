import pytest
import utils

from glaciers import *
from pytest import raises


"""以下测试用于测试适当的数据输入是否会顺利进行"""

@pytest.mark.parametrize( 'id',
                         ['12345',
                          '89201',
                          '04320'])
def test_validation_for_id( id ):
    assert utils.validation_for_id( id )








"""以下测试用于测试不当的数据输入是否会报出相应的错误"""

def test_validation_for_id_fail_on_non_5_length_id():
    with raises(ValueError) as e: 
        utils.validation_for_id( '782012' )

    exec_msg = e.value.args[0]
    assert exec_msg == "length of id should be 5"

def test_validation_for_id_fail_on_non_numeric_id():
    with raises(TypeError) as e: 
        utils.validation_for_id( '78SX1' )

    exec_msg = e.value.args[0]
    assert exec_msg == "id should be a integer"



"""以下测试用于测试add_mass_balance_measurement函数是否顺利读取了整体和局部测量的数据"""
    

"""以下测试用于测试filter_by_code函数是否适用于完整代码和非完整代码模式"""


"""以下测试用于测试sort_by_latest_mass_balance函数是否能够适用于不同方向的排序"""
