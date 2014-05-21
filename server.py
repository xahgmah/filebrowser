__author__ = 'shishov'

import os
import urlparse
from twisted.internet.protocol import ServerFactory, Protocol


class FileProtocol(Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.data)
        self.transport.loseConnection()


class FileFactory(ServerFactory):
    protocol = FileProtocol

    def __init__(self, path):
        self.data = self.readCatalogue(path)

    def readCatalogue(self, path):
        uploaddir = os.path.abspath('upload')
        data = ''
        path = "" if path == "" else path
        readdir = os.path.join(uploaddir, path)
        try:
            for element in os.listdir(readdir):

                if os.path.isdir(os.path.join(readdir, element)):
                    name = element + "/"
                else:
                    name = element
                data += "<a href='{0}'>".format(os.path.join(path, name))
                data += name
                data += "</a>"
                data += "<br/>"
        except IOError as e:
            data += "I/O error({0}): {1}".format(e.errno, e.strerror)

        data += "<br/>"
        data += "<br/>"
        for x in os.environ:
            data += x + "  -   " + os.environ[x] +"<br/>"
        return data


def main():
    data = ""

    factory = FileFactory(data)

    from twisted.internet import reactor

    port = reactor.listenTCP(10001, factory)

    reactor.run()


if __name__ == '__main__':
    main()