import argparse
import pytesseract
from PIL import Image
from PyPDF2 import PdfFileReader
from imutils import contours
import imutils
from pdf2image import convert_from_path
import cv2
import numpy as np

# get image coordinate
def get_boxes_coordinate(image):
    image = cv2.resize(image, (361, 500))

def printImage(image):
    cv2.imshow("my image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getInput():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inputFile", required=True,
                    help="path to image")  # -i để cho viết tắt trước khi truyền tham số còn không thì
    # ap.add_argument("-n","--outName",required = True, help = "name of docx")
    args = vars(ap.parse_args())
    return args["inputFile"]

def IOU(oldbox,newbox):
    (x1,y1,w1,h1) = oldbox
    (x2,y2,w2,h2) = newbox
    cx1 = x1 + w1/2
    cx2 = x2 + w2/2
    cy1 = y1 + h1/2
    cy2 = y2 + h2/2
    if cx1 >= x2 and cx1 <= x2+w2 and cy1>= y2 and cy1<= y2+h2:
        return True
    if cx2 >= x1 and cx2 <= x1+w1 and cy2>= y1 and cy2<= y1+h1:
        return True
    return False

def getTableCoordinate(image):
    """

    :param image:
    :return:
    listResult: x, y coordinates of layout 's bounding box
    listBigBox: x, y coordinates of table in image
    """
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((3, 3), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    (h1, w1) = image.shape
    blured = cv2.GaussianBlur(image, (11, 11), 0)
    canImage = cv2.Canny(blured, 100, 250)
    newimage = np.zeros_like(image)
    if imutils.is_cv2() or imutils.is_cv4():
        (conts, _) = cv2.findContours(canImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    elif imutils.is_cv3():
        (_, conts, _) = cv2.findContours(canImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    listBigBoxPoint = []
    listBigBox = []
    listPoint = []
    listResult = []
    if len(conts) > 0:
        conts = contours.sort_contours(conts)[0]
        # conts = sorted(conts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1] )
        for i in range(len(conts)):
            (x, y, w, h) = cv2.boundingRect(conts[i])
            if w > 10 and h > 10 and w < 0.7 * w1:
                if (x, y) not in listPoint:
                    for j in range(-5, 5, 1):
                        listPoint.append((x + j, y + j))
                    listResult.append((x, y, w, h))
                    cv2.rectangle(newimage, (x, y), (x + w, y + h), 255, 1)
                    # printImage(newimage)
            if w > 10 and h > 10 and w > 0.7 * w1:
                if (x, y) not in listBigBoxPoint:
                    listBigBox.append((x, y, w, h))
                    listBigBoxPoint.append((x, y))
    ## phuong phap xu li tam thoi
    return listResult, listBigBox

def compare_table(item1, item2):
    # return (item1[2]-item2[2])/10
    if (item1[2] - item2[2]) // 10 > 0:  # return 1 means swap
        return 1
    elif (item1[2] - item2[2]) // 10 < 0:
        return -1
    else:
        return item1[1] - item2[1]


def retreiveTextFromTable(listResult,image):
    results = []
    for cnt in listResult:
        x, y, w, h = cnt
        crop = image[y:y + h, x:x + w]
        output_tesseract = pytesseract.image_to_string(crop,
                                                lang='vie')
        if output_tesseract == '':
                continue
        results.append(output_tesseract)
    return results                                        