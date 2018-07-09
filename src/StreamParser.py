import numpy as np
import cv2
import os
import sys
import time

class StreamParser():

    def analyzeFootage(self, videoInputPath):

        capture = cv2.VideoCapture(videoInputPath)
        sift = cv2.xfeatures2d.SIFT_create()

        previous = {}
        current = {}

        previous["ret"], previous["frame"] = capture.read()
        previous["gray"] = cv2.cvtColor(previous["frame"], cv2.COLOR_BGR2GRAY)
        previous["blur"] = cv2.GaussianBlur(previous["gray"], (3, 3), 0)
        previous["keypoints"] = sift.detect(previous["blur"], None)
        previous["keypointsImage"] = cv2.drawKeypoints(previous["blur"], previous["keypoints"], previous["blur"])

        staticMap = np.zeros(previous["gray"].shape, dtype=np.uint8)
        max = 1

        for z in range(0, 100):

            current["ret"], current["frame"] = capture.read()
            current["gray"] = cv2.cvtColor(current["frame"], cv2.COLOR_BGR2GRAY)
            current["blur"] = cv2.GaussianBlur(current["gray"], (3, 3), 0)
            current["keypoints"] = []
            potentialKeypoints = sift.detect(current["blur"], None)

            for potentialKeypoint in potentialKeypoints:
                xa = int(potentialKeypoint.pt[0])
                ya = int(potentialKeypoint.pt[1])
                da = int(potentialKeypoint.size)
                aa = int(potentialKeypoint.angle)

                found = False

                for previousKeypoint in previous["keypoints"]:
                    xb = int(previousKeypoint.pt[0])
                    yb = int(previousKeypoint.pt[1])
                    db = int(previousKeypoint.size)
                    ab = int(previousKeypoint.angle)

                    if xa == xb and ya == yb and da == db and aa == ab:
                        found = True
                        break

                if found or staticMap[ya][xa] > max / 4:
                    staticMap[ya][xa] += 1

                    if staticMap[ya][xa] > max:
                        max = staticMap[ya][xa]
                else:
                    current["keypoints"].append(potentialKeypoint)

            current["keypointsImage"] = cv2.drawKeypoints(current["blur"], current["keypoints"], current["blur"], flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            print(z, "outof", 99, "max", max, flush=True)

            cv2.imwrite("output/reee/kps" + str(z) + ".jpg", current["keypointsImage"])

            previous["ret"] = current["ret"]
            previous["frame"] = current["frame"]
            previous["gray"] = current["gray"]
            previous["blur"] = current["blur"]
            previous["keypoints"] = current["keypoints"]
            previous["keypointsImage"] = current["keypointsImage"]

        (rows, cols) = staticMap.shape

        for y in range(0, rows):
            for x in range(0, cols):
                staticMap[y][x] = int(staticMap[y][x] * (255 / max))

        cv2.imwrite("output/reee/static.jpg", staticMap)

        capture.release()
