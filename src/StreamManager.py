from streamlink import Streamlink
import time
import sys
import os

class StreamManager():

    url             = None
    quality         = None
    logOutputPath   = None
    videoOutputPath = None
    session         = None

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

    def getLogOutputPath(self):
        if self.logOutputPath != None:
            return self.logOutputPath
        else:
            sys.exit("logOutputPath is not defined")

    def setLogOutputPath(self, logOutputPath):
        self.logOutputPath = logOutputPath

    def getVideoOutputPath(self):
        if self.videoOutputPath != None:
            return self.videoOutputPath
        else:
            sys.exit("videoOutputPath is not defined")

    def setVideoOutputPath(self, videoOutputPath):
        self.videoOutputPath = videoOutputPath

    ###########################################################################

    def getStream(self):

        url = self.getUrl()
        quality = self.getQuality()

        return self.session.streams(url)[quality]

    def getStreamObject(self):

        stream = self.getStream()

        return stream.open()

    def startScrape(self, start):

        streamObject = self.getStreamObject()

        logOutputPath   = self.getLogOutputPath()
        videoOutputPath = self.getVideoOutputPath()

        logFile = open(logOutputPath, "a")
        videoFile = open(videoOutputPath, "wb")

        average = -1
        sum = -1

        i = 0

        while i < 1024:

            if average == -1:

                data = streamObject.read(1024 * 1024 * 2)

            else:

                data = streamObject.read(average)

            before = os.stat(videoOutputPath).st_size

            videoFile.write(data)

            after = os.stat(videoOutputPath).st_size

            difference = after - before

            if difference != 0:

                i += 1

                if average == -1:

                    average = sum = after - before

                else:

                    sum = sum + difference
                    average = int(sum / i)

                duration = round(time.time() - start, 4)

                logString =     ""
                logString +=    "I: "       + str(i).zfill(8)           + ", "
                logString +=    "Time: "    + str(duration).zfill(10)   + ", "
                logString +=    "Before: "  + str(before).zfill(10)     + ", "
                logString +=    "After: "   + str(after).zfill(10)      + ", "
                logString +=    "Diff: "    + str(difference).zfill(7)  + ", "
                logString +=    "Average: " + str(average).zfill(7)     + "\n"

                logFile.write(logString)
                logFile.flush()

        logFile.close()
        videoFile.close()
        streamObject.close()

        return True

    ###########################################################################
