#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch


# This is a list of real SIP user-agents which have been
# handpicked from the wild. ;)
ualist = [
    'SIPp',
]

import random
from mutators.replparam import genRandStr

def randUASelect(randstr=False, length=30):
    if randstr:
        return genRandStr(length, allow_digits=True)
    else:
        return random.choice(ualist)