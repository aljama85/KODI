# coding: UTF-8
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