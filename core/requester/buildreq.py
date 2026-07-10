#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import os
import random, socket, re
from libs.config import *
from core.uaselect import randUASelect
from core.subjselect import randSubjSelect
from core.utils import extractExtension
from core.requester.parser import concatMethodxHeaders
from mutators.replparam import genRandStr

def makeRequest(method, bsbody=''):
    '''
    Build up the SIP request properly from scratch
    '''
    headers = { }
    extension = DEF_EXT
    branch = BRANCH
    body = ''
    contenttype = None
    srchost = socket.gethostbyname(socket.gethostname()) if not SRC_HOST else SRC_HOST
    dsthost = IP  # if IP else validateHost(RHOST)
    if 'invite' in method.lower():
        body = INVITE_BODY
        body = body.replace('x.x.x.x', srchost).replace('y.y.y.y', dsthost)
        # Randomize the SDP o= session-id / version per request so the
        # static template values do not leak the generator (benign-observed ranges)
        sess_id = random.randint(1767520664, 1767542828)
        sess_ver = random.randint(232, 999749)
        body = re.sub(r'(o=mhandley )\d+ \d+( IN IP4 )',
                      r'\g<1>%d %d\g<2>' % (sess_id, sess_ver), body)
    if bsbody:
        body = bsbody
    if extension is None or method.upper() == 'REGISTER':
        uri = 'sip:%s' % dsthost
    else:
        uri = 'sip:%s@%s:%s' % (extension, dsthost, RPORT)

    headers['Via'] = 'SIP/2.0/UDP %s:%s;branch=z9hG4bK-%s-1-1' % (srchost, LPORT, str(os.getpid()))

    if not FROM_ADDR:
        senderext = genRandStr(5)
        headers['From'] = '"siptorch" <sip:%s@%s>' % (senderext, RHOST)
    else:
        headers['From'] = FROM_ADDR
        senderext = extractExtension(FROM_ADDR)

    if not TO_ADDR:
        headers['To'] = '"%s" <sip:%s@%s>' % (DEF_EXT, DEF_EXT, RHOST)
    else:
        headers['To'] = TO_ADDR

    # If method is register, we need to modify To, From header fields
    if method == 'REGISTER':
        headers['From'] = '"%s" <sip:%s@%s>' % (extension, extension, RHOST)
        headers['To'] = headers['From']
    if method.lower() != 'ack':
        if FROM_TAG is None:
            headers['From'] += ';tag=%sSIPpTag' % str(os.getpid())
        else:
            headers['From'] += ';tag='+FROM_TAG

    if not STATIC_CID:
        headers["Call-ID"] = "1-" + str(os.getpid()) + "@" + srchost
    else:
        headers["Call-ID"] = CALL_ID

    headers['CSeq'] = '%s %s' % (CSEQ, method)

    if 'register' not in method.lower():
        headers['Contact'] = '<sip:%s@%s:%s>' % (senderext, srchost, LPORT)

    headers['Max-Forwards'] = 70

    if SPOOF_UA:
        headers['User-Agent'] = randUASelect()
    elif USER_AGENT:
        headers['User-Agent'] = USER_AGENT

    if 'invite' in method.lower():
        headers['Subject'] = randSubjSelect()

    if CONTENT_TYPE is not None and len(body) > 0:
        contenttype = CONTENT_TYPE
    elif len(body) > 0 and body.startswith('v=0'):
        # A normal (non-torture) SDP body must advertise its media type
        contenttype = 'application/sdp'
    if contenttype is not None:
        headers['Content-Type'] = contenttype

    headers['Content-Length'] = len(body)

    r = '%s %s SIP/2.0\r\n' % (method, uri)
    reformedmsg = concatMethodxHeaders(r, headers, body=body)
    return reformedmsg
