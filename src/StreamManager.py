from streamlink import Streamlink
import time
import sys
import os

class StreamManager():

    url                 = None
    quality             = None
    logOutputPath       = None
    videoOutputPath     = None
    session             = None
    scrapeEndConditon   = None
    scrapeEndValue      = None

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

    def getScrapeEndConditon(self):
        if self.scrapeEndConditon != None:
            return self.scrapeEndConditon
        else:
            sys.exit("scrapeEndConditon is not defined")

    def setScrapeEndConditon(self, scrapeEndConditon):
        self.scrapeEndConditon = scrapeEndConditon

    def getScrapeEndValue(self):
        if self.scrapeEndValue != None:
            return self.scrapeEndValue
        else:
            sys.exit("scrapeEndValue is not defined")

    def setScrapeEndValue(self, scrapeEndValue):
        self.scrapeEndValue = scrapeEndValue

    ###########################################################################

    def getStream(self):

        url = self.getUrl()
        quality = self.getQuality()

        return self.session.streams(url)[quality]

    def getStreamObject(self):

        stream = self.getStream()

        return stream.open()

    def checkScrapeEndConditon(self, iterations, timeDuration, fileSize):

        scrapeEndValue = self.getScrapeEndValue()
        scrapeEndConditon = self.getScrapeEndConditon()

        if scrapeEndConditon == "iterations":
            if iterations >= scrapeEndValue:
                return False
            else:
                return True
        elif scrapeEndConditon == "timeDuration":
            if timeDuration >= scrapeEndValue:
                return False
            else:
                return True
        elif scrapeEndConditon == "fileSize":
            if fileSize >= scrapeEndValue:
                return False
            else:
                return True
        else:
            sys.exit("scrapeEndConditon does not match a supported condition i.e. (iterations, timeDuration, fileSize)")

    def startScrape(self, start):

        streamObject = self.getStreamObject()

        logOutputPath   = self.getLogOutputPath()
        videoOutputPath = self.getVideoOutputPath()

        logFile = open(logOutputPath, "a")
        videoFile = open(videoOutputPath, "wb")

        i = 0
        sum = -1
        average = -1
        currentSize = os.stat(videoOutputPath).st_size
        duration = round(time.time() - start, 4)

        while self.checkScrapeEndConditon(i, duration, currentSize):

            if average == -1:

                data = streamObject.read(1024 * 1024 * 2)

            else:

                data = streamObject.read(average)

            before = os.stat(videoOutputPath).st_size

            videoFile.write(data)

            after = currentSize = os.stat(videoOutputPath).st_size

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
