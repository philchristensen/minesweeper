"""
Minesweeper example client.
"""

from pyamf.remoting.client import RemotingService
gateway = RemotingService('http://localhost:8080/amf')
render = gateway.getService('minesweeper.render')
print render()