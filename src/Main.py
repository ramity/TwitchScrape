from StreamManager import StreamManager
import sys

def main():

    streamManager = StreamManager()

    streamManager.setUrl("https://www.twitch.tv/emongg")
    streamManager.setQuality("best")

    streamObject = streamManager.getStreamObject()

    data = streamObject.read(1024)

    print("test")

    print(sys.getsizeof(data))
    print(len(data))

main()
