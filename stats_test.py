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


def test_mean_with_pop_variance(n: int, target_mean: float, sample_mean: float, pop_variance: float, significance: float, side: Side) -> (bool, float):
    """
    平均値に関するz検定を行う．

    ## Parameters  
    `n`: 標本の大きさ  
    `target_mean`: 帰無仮説において等しいと仮定する平均値  
    `sample_mean`: 標本平均  
    `pop_variance`: 既知の母分散  
    `significance`: 有意水準  
    `side`: 棄却域の取り方

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか
    """

    z = (sample_mean - target_mean) / math.sqrt(pop_variance / n)
    bottom = stats.norm.ppf((1 - significance) / 2)
    top = stats.norm.ppf((1 + significance) / 2)
    bottom_left = stats.norm.ppf(1 - significance)
    top_right = stats.norm.ppf(significance)
    print(bottom, top)
    return (is_reject(z, side, bottom, top, bottom_left, top_right), z)
