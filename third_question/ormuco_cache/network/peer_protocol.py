from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import protocol

from ormuco_cache.network import *
from ormuco_cache.repository.network import ServerNetworkRepository

class PeerProtocol(LineReceiver):
    def __init__(self, command_parser):
        self.command_parser = command_parser

    def connectionMade(self):
        self.sendLine(b"PEER")
        ServerNetworkRepository.peer_protocols.add(self)

    def lineReceived(self, line):
        decoded_line = line.decode("utf-8")
        if decoded_line != 'ACK':
            ServerNetworkRepository.last_peer = self
            self.command_parser.parse(line.decode("utf-8"))


class PeerProtocolFactory(ReconnectingClientFactory):
    def __init__(self, command_parser):
        self.peers = set()
        self.command_parser = command_parser
 
    def buildProtocol(self, addr): 
        self.resetDelay()
        return PeerProtocol(self.command_parser)

    def clientConnectionLost(self, connector, reason):
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
