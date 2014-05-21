__author__ = 'shishov'

import sys
import urllib2


class Uploader():
    def __init__(self):
        if len(sys.argv) > 1:
            self.url = (sys.argv[1])
        else:
            print ("Invalid url")
        self.upload_file()


    def upload_file(self):
        file_name = self.url.split('/')[-1]
        u = urllib2.urlopen(self.url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
        f.close()

class Mp3Uploader(Uploader):
    def __init__(self):
        self.url = u'https://dl.dropboxusercontent.com/u/102471963/The%20Pixies%20-%20Where%20Is%20My%20Mind.mp3'
        Uploader()


Mp3Uploader()