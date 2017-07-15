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

    test_image = cv2.imread("BaseLib/LicPlateImages/3.png")
    if test_image is None:
        print "Failed to load test data"

    plates = DetectPlates.detectPlatesInScene(test_image)
    chars = DetectChars.detectCharsInPlates(plates)

    best_fit = None

    for char in chars:
        if best_fit is None:
            best_fit = char.strChars
        else:
            if len(char.strChars) == 6:
                best_fit = char.strChars

    print "Best Fit: " + best_fit

if __name__ == '__main__':
    run()
