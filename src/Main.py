from StreamManager import StreamManager
from StreamParser import StreamParser
import time
import sys

def main():

    streamParser = StreamParser()
    streamParser.analyzeFootage("./output/1530837385.423015.avi")
    sys.exit(0)

    streamManager = StreamManager()

    start = time.time()

    streamManager.setUrl("https://www.twitch.tv/linkzr")
    streamManager.setQuality("best")
    streamManager.setLogOutputPath("./output/" + str(start) + ".log")
    streamManager.setVideoOutputPath("./output/" + str(start) + ".avi")
    streamManager.setScrapeEndConditon("fileSize")
    streamManager.setScrapeEndValue(10000000000)

    streamManager.startScrape(start)

main()
