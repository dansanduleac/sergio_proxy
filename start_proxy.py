#!/usr/bin/env python
from twisted.web import http
from twisted.internet import reactor
from sergio_proxy import transparent_proxy
from UserMITM import UserMITM


import sys
from twisted.python.log import startLogging
startLogging(open("twisted.log", "w"), setStdout=False)

transparent_proxy.mitm = UserMITM()
# Show the state of the mitm
print transparent_proxy.mitm

# TransparentProxy is essentially a HTTPChannel
# so it can be used as the protocol for a HTTPFactory
f = http.HTTPFactory()
f.protocol = transparent_proxy.TransparentProxy
# make the HTTPFactory listen
reactor.listenTCP(8081, f)
# run the reactor
reactor.run()
