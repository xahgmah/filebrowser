__author__ = 'shishov'

from twisted.internet.protocol import ServerFactory, Protocol


class FileProtocol(Protocol):

    def connectionMade(self):
        self.transport.write(self.factory.data)
        self.transport.loseConnection()


class FileFactory(ServerFactory):

    protocol = FileProtocol

    def __init__(self, data):
        self.data = data


def main():

    data = 'TEST DATA here'

    factory = FileFactory(data)

    from twisted.internet import reactor

    port = reactor.listenTCP(10000, factory)

    reactor.run()


if __name__ == '__main__':
    main()