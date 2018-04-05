from streamlink import Streamlink
import sys

class StreamManager():

    url         = ""
    quality     = "best"
    outputPath  = "../video/decoded/"

    #stream

    def __init__(self):

        session = Streamlink()
        session.set_loglevel("info")
        session.set_logoutput(sys.stdout)

        self.session = session

    ###########################################################################

    def getUrl(self):
        if self.url != None:
            return self.url
        else:
            sys.exit("url is not defined")

    def setUrl(self, url):
        self.url = url

    def getQuality(self):
        if self.quality != None:
            return self.quality
        else:
            sys.exit("quality is not defined")

    def setQuality(self, quality):
        self.quality = quality

    def getOutputPath(self):
        if self.outputPath != None:
            return self.outputPath
        else:
            sys.exit("outputPath is not defined")

    def setOutputPath(self, outputPath):
        self.outputPath = outputPath

    ###########################################################################

    def getStream(self, url, quality):

        if url == None:
            sys.exit("url not defined")

        if quality == None:
            sys.exit("quality not defined")

        return self.session.streams(self.url)[self.quality]

    def getStreamObject(self):

        stream = self.getStream(self.url, self.quality)

        if stream == None:
            sys.exit("stream not defined")

        return stream.open()

    def closeStreamObject(self, streamObject):

        if streamObject == None:
            sys.exit("streamObject is not defined")

        streamObject.close()

    ###########################################################################
