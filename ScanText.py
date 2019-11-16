import pytesseract
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
    
    return result