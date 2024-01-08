import cv2 as cv
import numpy as np
from Classification_Functions import  checkDistance

def Treble_Classification(img_gray, img_rgb, template_file, threshold):

    template = cv.imread(template_file, cv.IMREAD_GRAYSCALE)
    treble_w, treble_h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    treble_pt_list = []

    #draws rectangles
    for pt in zip(*loc[::-1]):
        if checkDistance(treble_pt_list, pt, 50):
            treble_pt_list.append(pt)
            cv.rectangle(img_rgb, pt, (pt[0] + treble_w, pt[1] + treble_h), (0,255,0), 2)
    
    treble_list = []
    for treble_pt in treble_pt_list:
         treble_list.append([treble_pt, "treble", (treble_w, treble_h)])

    return treble_list