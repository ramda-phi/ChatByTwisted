

from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from sys import stdout


class Echo(Protocol):
    def dataReceived(self, data):
        stdout.write(data)


class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return Echo()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed.  Reason:', reason


reactor.connectTCP(host, port, EchoClientFactory())
reactor.run()
