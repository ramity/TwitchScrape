from StreamManager import StreamManager
from StreamParser import StreamParser
import time
import sys

def main():

    streamParser = StreamParser()

    streamParser.analyzeFootage("./output/1523129683.8167825.avi")

    sys.exit(0)

    streamManager = StreamManager()

    start = time.time()

    streamManager.setUrl("https://www.twitch.tv/pvptwitch")
    streamManager.setQuality("best")
    streamManager.setLogOutputPath("./output/" + str(start) + ".log")
    streamManager.setVideoOutputPath("./output/" + str(start) + ".avi")
    streamManager.setScrapeEndConditon("iterations")
    streamManager.setScrapeEndValue(100)

    streamManager.startScrape(start)

main()
