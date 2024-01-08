
import sys
from find_scale import scaleImage
from Treble_Classification import Treble_Classification
from Bass_Classification import Bass_Classification
from BarLine_Classification import BarLine_Classification
from CreateBarBoxes import CreateBarBoxes
from node_recognition_output import note_recognition
from Structure_Data import Structure_Data
from remove_detect_line import detectionLine, removeLine
from Determine_Note import Determine_Note
from export_mxl import export
import cv2 as cv


def main(imagePath, outputName):    
    scaleImage(imagePath, "./data/images/rescaleOutput.png")
    
    removeLine(cv.imread('./data/images/rescaleOutput.png'), 10, './data/images/removeLineOutput.png')

    img_rgb = cv.imread('./data/images/removeLineOutput.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    treble_list = Treble_Classification(img_gray, img_rgb, './data/templates/treble.png', 0.5)
    bass_list = Bass_Classification(img_gray, img_rgb, './data/templates/bass.png', 0.5)
    barline_list = BarLine_Classification(img_gray, img_rgb, './data/templates/vertical_line.png', 0.8)
    
    barline_w, barline_h = (cv.imread('./data/templates/vertical_line.png', cv.IMREAD_GRAYSCALE)).shape[::-1]

    barbox_list = CreateBarBoxes(treble_list, bass_list, barline_list, barline_w, barline_h, img_gray, img_rgb)

    line_list = detectionLine("./data/images/rescaleOutput.png", "./data/templates/staff line.png", 0.9)
    notation_list = note_recognition(line_list, './data/images/removeLineOutput.png')

    for element in notation_list:
        cv.rectangle(img_rgb, element[0], (element[0][0] + element[2][0], element[0][1] + element[2][1]), (100,100,100), 2)
        cv.putText(img_rgb, element[1], element[0], cv.FONT_HERSHEY_SIMPLEX, 0.8, (10,169,21), 2)

    cv.imwrite('./data/images/testOutput.png', img_rgb)

    structured_notation_list = Structure_Data((treble_list + bass_list + notation_list), barbox_list)
    structured_notation_list = Determine_Note(line_list, structured_notation_list, img_gray, 0.70)

    export(structured_notation_list, "musicxml", "./data/music-xmls/" + outputName + ".mxl", outputName)

    return 0


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])