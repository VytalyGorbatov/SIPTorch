#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging, random
from libs import config
from core.plugrun import runPlugin
from core.requester import buildreq
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.fuzzutils import random_digits, random_int_str

module_info = {
    'category'  :   'Application Layer Semantics',
    'test'      :   'Multiple Values in Single Value Required Fields',
    'id'        :   'multireq'
}

def multireq():
    '''
    Multiple Values in Single Value Required Fields

    An element receiving this request would respond with a 400 Bad
    Request error.
    '''
    log = logging.getLogger('multireq')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('INVITE')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Add multiple keys with same value duplicate
    # The RFC 3261 says that the SIP message is not case-sensitive
    # So what we do to exploit this is, lowercase the keys to form 
    # duplicates, since in no way a dict can hold duplicates
    #
    # Duplicating the following fields - call-id, to, from, max-
    # forwards, cseq headers
    head['call-id'] = random.getrandbits(80)
    head['cseq'] = '%s INVITE' % random_int_str(50, 900)
    head['to'] = 'sip:%s@%s' % (random_digits(3, 6), config.RHOST)
    head['from'] = 'sip:%s@%s;tag=%s' % (
        random_digits(3, 6), config.RHOST, random.getrandbits(32))
    head['max-forwards'] = random_int_str(1, 20)
    # Recompiling our message
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(multireq(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
