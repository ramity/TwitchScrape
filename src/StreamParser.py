import numpy as np
import cv2
import os
import sys
import time

class StreamParser():

    def analyzeFootage(self, videoInputPath):

        capture = cv2.VideoCapture(videoInputPath)

        while(capture.isOpened()):

            ret, frame = capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(frame, (5, 5), 0)
            edge = cv2.Canny(blur, 50, 150)

            cv2.imshow("frame", edge)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()
