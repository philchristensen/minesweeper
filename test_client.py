# Copyright (c) 2007-2009 The PyAMF Project.
# See LICENSE.txt for details.

"""
Hello world example client.

@see: U{HelloWorld<http://pyamf.org/wiki/HelloWorld>} wiki page.

@since: 0.1.0
"""

from pyamf.remoting.client import RemotingService

gateway = RemotingService('http://localhost:8080/amf')

render = gateway.getService('minesweeper.render')

print render()