from scipy import stats
from enum import Enum
import math


class Side(Enum):
    """
    棄却域の取り方を表現する．

    ## Attributes  
    `DOUBLE`: 両側検定  
    `LEFT`: 左片側検定  
    `RIGHT`: 右片側検定
    """

    DOUBLE = 1
    LEFT = 2
    RIGHT = 3


def side_from_str(side: str) -> Side:
    if side == "double":
        return Side.DOUBLE
    elif side == "left":
        return Side.LEFT
    elif side == "right":
        return Side.RIGHT
    else:
        return None


def is_reject(test_stats: float, side: Side, bottom: float, top: float, bottom_left: float, top_right: float) -> bool:
    """
    帰無仮説が棄却されるかどうかを返す．

    ## Parameters  
    `test_stats`: 帰無仮説のもとでの統計検定量  
    `side`: 棄却域の取り方  
    `bottom`: 棄却域の下限  
    `top`: 棄却域の上限  
    `bottom_left`: 棄却域の下限(左片側検定)  
    `top_right`: 棄却域の下限(右片側検定)  

    ## Returns  
    `is_rejected`: 帰無仮説が棄却されるかどうか
    """

    if side == Side.DOUBLE or side == None:
        if test_stats < bottom or test_stats > top:
            return True
        else:
            return False
    elif side == Side.LEFT:
        if test_stats < bottom_left:
            return True
        else:
            return False
    else:
        if test_stats > top_right:
            return True
        else:
            return False


def show_result(is_reject: bool, test_stat: float, hypothesis: float):
    result_str = "実現値: {}\n".format(test_stat)
    if is_reject:
        result_str += "帰無仮説 'μ = {}' は棄却されました".format(hypothesis)
    else:
        result_str += "帰無仮説 'μ = {}' は採択されました".format(hypothesis)
    return result_str
