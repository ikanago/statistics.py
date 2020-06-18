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


def is_reject(test_stats: float, side: Side, bottom: float, top: float) -> bool:
    """
    帰無仮説が棄却されるかどうかを返す．

    ## Parameters  
    `test_stats`: 帰無仮説のもとでの統計検定量  
    `side`: 棄却域の取り方  
    `bottom`: 棄却域の下限  
    `top`: 棄却域の上限

    ## Returns  
    `is_rejected`: 帰無仮説が棄却されるかどうか
    """

    if side == Side.DOUBLE or side == None:
        if test_stats < bottom or test_stats > top:
            return True
        else:
            return False
    elif side == Side.LEFT:
        if test_stats < bottom:
            return True
        else:
            return False
    else:
        if test_stats > top:
            return True
        else:
            return False


def test_mean_with_pop_variance(target_mean: float, sample_mean: float, pop_variance: float, n: int, significance: float, side: Side) -> bool:
    """
    平均値に関するz検定を行う．

    ## Parameters  
    `target_mean`: 帰無仮説において等しいと仮定する平均値  
    `sample_mean`: 標本平均  
    `pop_variance`: 既知の母分散  
    `n`: 標本の大きさ  
    `significance`: 有意水準  
    `side`: 棄却域の取り方

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか
    """

    z = (sample_mean - target_mean) / math.sqrt(pop_variance / n)
    bottom = stats.norm.ppf(1 - significance / 2)
    top = stats.norm.ppf(significance / 2)
    return is_reject(z, side, bottom, top)
