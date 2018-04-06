from StreamManager import StreamManager
import time

def main():

    streamManager = StreamManager()

    start = time.time()

    streamManager.setUrl("https://www.twitch.tv/xqcow")
    streamManager.setQuality("best")
    streamManager.setLogOutputPath("./output/" + str(start) + ".log")
    streamManager.setVideoOutputPath("./output/" + str(start) + ".avi")

    streamManager.startScrape(start)

main()
