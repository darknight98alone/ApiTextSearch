import pytesseract
from handleTable import IOU,printImage
import cv2
import imutils


def GetText(listResult,listBigBox,img):
    result = []
    (height,_) = img.shape[:2]
    if len(listBigBox)==0:
        result.append(pytesseract.image_to_string(img,lang='vie')+"\n")
        return result
    bigBoxTemp = []
    listYCoord = []
    listYCoord.append(0)
    for (_,y,_,h) in listBigBox:
        bigBoxTemp.append((y,y+h))
        listYCoord.append(y)
        listYCoord.append(y+h)
    listYCoord.append(height)
    for index,y1 in enumerate(listYCoord):
        if index == len(listYCoord)-1:
            break
        y2 = listYCoord[index+1]
        if (y1,y2) not in bigBoxTemp:
            crop = img[y1:y2,:]
            result.append(pytesseract.image_to_string(crop,lang='vie')+"\n")
        else:
            index = 0
            box = listBigBox.pop(0)
            for temp in listResult:
                if IOU(temp[0],box):
                    index = index +1
                    for (x,y,w,h) in temp:
                        crop = img[y:y+h,x:x+w]
                        size = int(crop.shape[0]*1.5)
                        if size < 100:
                            size = 100
                        crop = imutils.resize(crop,height=size) ## 
                        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                        idx = (crop.flatten()<5)
                        temp = sum(idx[:])
                        if temp <2:
                            continue
                        string  = pytesseract.image_to_string(crop,lang='vie')
                        if len(string) == 0:
                            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
                            crop = cv2.erode(crop, kernel, iterations=1)
                            while size<=200:
                                string  = pytesseract.image_to_string(crop,lang='eng',config='--psm 10')
                                if ("l" in string or "I" in string ) and len(string)<3:
                                    string = "1"
                                if string.isdigit() or (len(string)>=2 and "," not in string and "'" not in string):
                                    break
                                size = size + 10
                                crop = imutils.resize(crop,height=size)
                        string = string + " "
                        string = string.replace("\n"," ")
                        result.append(string)
                    result.append("\n")
                else:
                    break
            listResult = listResult[index:]
    return result