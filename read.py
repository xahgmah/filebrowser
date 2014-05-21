__author__ = 'shishov'

# import os
from twisted.internet import protocol, reactor


# uploaddir =os.path.abspath('upload')
# try:
#     for element in os.listdir(uploaddir):
#         res = element+"/" if os.path.isdir(os.path.join(uploaddir, element)) else element
#         print(res)
# except IOError as e:
#     print "I/O error({0}): {1}".format(e.errno, e.strerror)

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)
        print(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

reactor.listenTCP(1234, EchoFactory())
reactor.run()