import pytesseract
from handleTable import IOU,printImage
def GetText(listResult,listBigBox,img):
    result = []
    if len(listBigBox)==0:
        result.append(pytesseract.image_to_string(img,lang='vie'))
        return result
    bigBoxTemp = []
    listYCoord = []
    listYCoord.append(0)
    (height,_) = img.shape[:2]
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
            result.append(pytesseract.image_to_string(crop,lang='vie'))
        else:
            index = 0
            box = listBigBox.pop(0)
            for temp in listResult:
                if IOU(temp[0],box):
                    index = index +1
                    for (x,y,w,h) in temp:
                        crop = img[y:y+h,x:x+w]
                else:
                    break
            listResult = listResult[index:]
        printImage(crop)
    return result