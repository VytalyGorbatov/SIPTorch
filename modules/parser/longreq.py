#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging
import string
from libs import config
from core.plugrun import runPlugin
from core.requester import buildreq
from mutators.multihead import multiHead
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.fuzzutils import random_domain, random_sentence, random_text, random_unknown_param, repeat_char, repeat_token

module_info = {
    'category'  :   'Syntactical Parser Tests',
    'test'      :   'Long Values in Header Fields',
    'id'        :   'longreq'
}

def longreq():
    '''
    Long Values in Header Fields

    This well-formed request contains header fields with many values and
    values that are very long.
    '''
    log = logging.getLogger('longreq')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('INVITE')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Such long To value
    longto = random_sentence((8, 12)) + repeat_token((5, 9), (9, 14))
    head['To'] = "%s <%s" % (longto, head.get('To').split('<')[1])
    head['To'] += ';%s=%s' % (
        random_unknown_param(), random_text() + repeat_char('o', 50, 80))
    head['To'] += ';%s=%s' % (
        random_unknown_param(prefix=''), random_text((1,1)) )
    head['To'] += random_text() + repeat_token((4, 7), (8, 12))
    # Tweak 2: Such long From Value
    head['From'] = 'sip:%s@%s' % (repeat_token((6, 10), (8, 12)), config.RHOST)
    head['From'] += ';tag=10%s420' % repeat_char(string.digits, 60, 120)
    head['From'] += ';%s=%s' % (
        random_unknown_param(prefix=''), repeat_token((5, 9), (7, 11)))
    head['From'] += random_text((1, 3)) + repeat_token((5, 8), (6, 10))
    # Tweak 3: add call id
    head['Call-ID'] = random_text() + repeat_token((6, 9), (7, 12))
    # Tweak 4: add contact
    head['Contact'] = '<sip:%s@%s>' % (
        repeat_token((6, 9), (8, 12)), config.RHOST)
    # Tweak 5: add unknown value
    key = '%s-L%sng-Field' % (random_text((1,1)), repeat_char('o', 40, 75))
    head[key] = '%s;%s=%s' % (
        '%s-%s-value' % (random_text((1,1)), repeat_token((4, 7), (6, 10))),
        '%s-%s-parameter-name' % (random_text((1,1)), repeat_token((4, 7), (5, 9))),
        '%s-%s-parameter-value' % (random_text((1,1)), repeat_token((4, 7), (6, 9)))
    )
    # Tweak 6: multiply the number of via headers
    pset = multiHead('Via', permuteasdict=True, singlestr=False)
    # Merging both the dicts together
    try:
        newhead = { **pset, **head }
    except Exception as e:
        log.error('Action not supported: %s' % e.__str__())
        newhead = pset.copy()
        newhead.update(head)
    sipc = 1
    for x in newhead.keys():
        if not newhead.get(x):
            newhead[x] = 'SIP/2.0/UDP sip%s.%s' % (sipc, random_domain())
            sipc += 1  # incrementing the value properly
    # Forming the message up back again
    mg = concatMethodxHeaders(mline, newhead, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(longreq(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
