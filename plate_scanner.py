import sys
import os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "BaseLib"))

import DetectChars
import cv2
import DetectPlates
import PossibleChar
import PossiblePlate
import Preprocess


def run():
    trainingData = DetectChars.loadKNNDataAndTrainKNN()

    if trainingData == False:
        print "Invalid Training Data"
        return

    test_image = cv2.imread("BaseLib/LicPlateImages/1.png")
    if test_image is None:
        print "Failed to load test data"

if __name__ == '__main__':
    run()
