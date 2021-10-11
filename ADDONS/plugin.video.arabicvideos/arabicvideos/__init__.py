# -*- coding: utf-8 -*-
import sys
l11ll11_ll_ = sys.version_info [0] == 2
l11111_ll_ = 2048
l111l_ll_ = 7
def l111lll_ll_ (ll_ll_):
    global l11lll1_ll_
    l11l1_ll_ = ord (ll_ll_ [-1])
    l11lll_ll_ = ll_ll_ [:-1]
    l11l_ll_ = l11l1_ll_ % len (l11lll_ll_)
    l111_ll_ = l11lll_ll_ [:l11l_ll_] + l11lll_ll_ [l11l_ll_:]
    if l11ll11_ll_:
        l1l1lll_ll_ = unicode () .join ([unichr (ord (char) - l11111_ll_ - (l1l11l_ll_ + l11l1_ll_) % l111l_ll_) for l1l11l_ll_, char in enumerate (l111_ll_)])
    else:
        l1l1lll_ll_ = str () .join ([chr (ord (char) - l11111_ll_ - (l1l11l_ll_ + l11l1_ll_) % l111l_ll_) for l1l11l_ll_, char in enumerate (l111_ll_)])
    return eval (l1l1lll_ll_)
from l1l1l1_ll_ import *
l1111111_ll_(l111lll_ll_ (u"ࠩࡑࡓ࡙ࡏࡃࡆࠩ䛰"),l111lll_ll_ (u"ࠪࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠪ䛱"))
#import l11_ll_,l1l1lll1_ll_,l1ll111_ll_,l111ll1l_ll_,l1ll11l11_ll_,l1l1ll11l_ll_,l1l1l111l_ll_,l11lll111_ll_,l111llll1_ll_,l111l11ll_ll_,l1llllll1l_ll_,l1l1l1l1l1_ll_,l11lll1ll1_ll_,l11l11111l_ll_,l111111lll_ll_,l1lll11l1l1_ll_,l1l1l111lll_ll_,l11l11ll1l1_ll_,l1l111l1111_ll_,l11l11lll1l_ll_,l1ll11llll1_ll_,l11l1ll1lll_ll_,l1ll1111l1l_ll_,l1l1ll11l11_ll_,l1l11l1l11l_ll_,l11ll1l1ll_ll_
#import l1_ll_,l1l1l1_ll_,l1ll1ll1l1_ll_,l11l11l1l1l_ll_,l11l1ll11l_ll_,l1ll1l11l11_ll_,l1l111111ll_ll_
#import EXCLUDES,l1l1ll11ll1l_ll_.cipher,l1l1ll11ll1l_ll_.l1l1l1llllll_ll_
l1ll111l1_ll_(l111lll_ll_ (u"ࠫࡸࡺࡡࡳࡶࠪ䛲"))
try: l111l1l_ll_()
except Exception as error: l1l11llll11_ll_(error)
l1ll111l1_ll_(l111lll_ll_ (u"ࠬࡹࡴࡰࡲࠪ䛳"))