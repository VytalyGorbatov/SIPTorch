#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging, re
from core.plugrun import runPlugin
from core.requester import buildreq
from mutators.urlencchar import urlEncodeStrInvalid
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.fuzzutils import random_digits

module_info = {
    'category'  :   'Syntactical Parser Tests',
    'test'      :   'Use of "%" When It Is Not an Escape',
    'id'        :   'escinv'
}

def escinv():
    '''
    Use of % When It Is Not an Escape

    In most of the places % can appear in a SIP message, it is not an
    escape character.  This can surprise the unwary implementor.
    A parser should accept this message as well formed.  A proxy would
    forward or reject the message depending on what the Request-URI meant
    to it.  An endpoint would reject this message with a 501.
    '''
    log = logging.getLogger('escinv')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: modify the register header
    newmeth = urlEncodeStrInvalid('EGISTER', randomchoice=True, value=2)
    # Making sure the first byte is not URL encoded
    newmeth = '%s%s' % ('R', newmeth)
    mline = mline.replace(mline.split(' ')[0], newmeth)
    # Tweak 2: Modify the to and from headers
    head['To'] = re.sub(r'\"\w+?\"', '"%Z%45"', head.get('To'))
    head['From'] = re.sub(r'\"\w+?\"', '"%Z%45"', head.get('From'))
    # Tweak 3: Change the Cseq header
    head['CSeq'] = '%s %s' % (head.get('CSeq').split(' ')[0], newmeth)
    # Tweak 4: Change a contact header, guarding against missing Contact
    contact_value = head.get('Contact')
    if not isinstance(contact_value, str) or contact_value.strip() == '':
        fallback_host = 'invalid'
        to_header = head.get('To')
        if isinstance(to_header, str) and '@' in to_header:
            fallback_host = to_header.split('@', 1)[-1].split('>')[0].strip()
        contact_value = '<sip:fallback@%s>' % fallback_host
        head['Contact'] = contact_value
    newct = '%s%s' % ('C', urlEncodeStrInvalid('ontact', value=1))
    head[newct] = re.sub(
        r'sip:\w+?@', 'sip:%s@' % random_digits(3, 5), contact_value)
    # Forming the message up back again
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(escinv(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
