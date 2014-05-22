__author__ = 'shishov'

import os
import urllib
from twisted.web import server, resource
import eyeD3

class FileBrowser(resource.Resource):
    isLeaf = True
    allowedMethods = ("GET", "POST")

    def render(self, request):
        if request.method == "GET":
            if "/favicon.ico" != request.uri:
                path = os.path.join(os.path.abspath('upload'), request.uri[1:])
                if os.path.isdir(path):
                    return self.readCatalogue(request, request.uri)
                else:
                    return self.sendFile(request, urllib.unquote(path))

        elif request.method == "POST":
            with open('test.mp3',  'w+') as fd:
                fd.write(request.args['file'][0])
            tag = eyeD3.Tag()
            tag.link("test.mp3")
            uploaddir = os.path.abspath(os.path.join('upload', tag.getArtist()) )
            if not os.path.isdir(uploaddir):
                os.makedirs(uploaddir)
            os.rename(os.path.abspath("test.mp3"),os.path.abspath(os.path.join('upload', tag.getArtist(),tag.getTitle()+".mp3")))
            print tag.getTitle()
            return 'Done'

    def readCatalogue(self, request, path):
        request.setHeader("Content-type", "text/html; charset=utf-8")
        uploaddir = os.path.abspath('upload')
        data = ''
        path = path[1:] if path[0] == "/" else path
        readdir = os.path.join(uploaddir, path)
        if path != "":
            data += "<a href='{0}'>../</a>".format("/" + "/".join(path[:-1].split("/")[:-1])) + "<br/>"
        try:
            for element in os.listdir(readdir):

                if os.path.isdir(os.path.join(readdir, element)):
                    name = element + "/"
                else:
                    name = element
                data += "<a href='{0}'>".format("/" + os.path.join(path, name))
                data += urllib.unquote(name)
                data += "</a>"
                data += "<br/>"
        except IOError as e:
            data += "I/O error({0}): {1}".format(e.errno, e.strerror)

        return data

    def sendFile(self, request, path):
        fd = open(path, 'r')
        request.setHeader("Content-Description", "File Transfer")
        request.setHeader("Expires", "0")
        request.setHeader("Content-Type", "application/octet-stream")
        request.setHeader("Content-Length", os.stat(path).st_size)
        # request.setHeader("Content-Type", "audio/mpeg")
        request.setHeader("Content-Disposition",
                          "attachment; filename='{0}'".format(os.path.basename(path)), )
        return fd.read()
        fd.close()


def main():
    site = server.Site(FileBrowser())

    from twisted.internet import reactor

    port = reactor.listenTCP(10001, site)

    reactor.run()


if __name__ == '__main__':
    main()