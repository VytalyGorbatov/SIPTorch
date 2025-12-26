#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging
from core.plugrun import runPlugin
from core.requester import buildreq
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.fuzzutils import random_int_str, random_reason_phrase

module_info = {
    'category'  :   'Syntactical Parser Tests',
    'test'      :   'Unusual Reason Phrase',
    'id'        :   'unreason'
}

def unreason():
    '''
    Unusual Reason Phrase

    This 200 response contains a reason phrase other than "OK".  The
    reason phrase is intended for human consumption and may contain any
    string produced by

        Reason-Phrase   =  *(reserved / unreserved / escaped
                            / UTF8-NONASCII / UTF8-CONT / SP / HTAB)

    This particular response contains unreserved and non-ascii UTF-8
    characters.  This response is well formed.  A parser must accept this
    message.
    '''
    log = logging.getLogger('unreason')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('INVITE')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Modify the header of the message
    # We are using a 20 char to form the remaining
    expr_one = '%s**%s' % (random_int_str(2, 9), random_int_str(2, 5))
    expr_two = '%s**%s' % (random_int_str(2, 9), random_int_str(2, 5))
    mline = 'SIP/2.0 200 = %s * %s %s' % (
        expr_one, expr_two, random_reason_phrase())
    # Forming the message up back again
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(unreason(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
