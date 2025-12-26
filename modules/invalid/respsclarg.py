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
from mutators.fuzzutils import random_huge_numeric_string, random_int_str
from mutators.fuzzutils import random_warning_agent, random_warning_text

module_info = {
    'category'  :   'Invalid Messages',
    'test'      :   'Response Scalar Fields with Overlarge Values',
    'id'        :   'respsclarg'
}

def respsclarg():
    '''
    Response Scalar Fields with Overlarge Values

    This response contains several scalar header field values outside
    their legal range (>2**32-1). Note that the Warning header too has 
    value greater than 3 digits. An element receiving this response will 
    simply discard it.
    '''
    log = logging.getLogger('respsclarg')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Modify the method line
    mline = 'SIP/2.0 503 Service Unavailable'
    # Tweak 2: Add retry after header
    head['Retry-After'] = random_huge_numeric_string(12, 28)
    # Tweak 3: Add warning header
    head['Warning'] = '%s %s "%s"' % (
        random_int_str(1000, 9999), random_warning_agent(),
        random_warning_text())
    # Tweak 4: Add large scalar value in cseq
    head['CSeq'] = head.get('CSeq').replace(
        head.get('CSeq').split(' ')[0], random_huge_numeric_string(12, 28))
    # Forming the message up back again
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(respsclarg(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
