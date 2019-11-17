import argparse
import pytesseract
from PIL import Image
from PyPDF2 import PdfFileReader
from imutils import contours
from pdf2image import convert_from_path
from skew import skewImage
from DetectTable import detectTable
from handleTable import getTableCoordinate,retreiveTextFromTable,getInput
from ScanText import GetText
import os
import imutils
import cv2
from docx import Document
from PdfToImages import pdfToImage

def handleFile(fileName,skew = False,deblur=False,handleTableBasic=True,handleTableAdvance=False):
    """
    :param fileName: name of image to be converted
    :param outputName: name of doc file to be saved
    :return:

    detect table and layout-analyzing
    """
    img = cv2.imread(fileName)
    
    # handle skew
    if skew:
        img = skewImage(img)
    # skew.printImage(img)
    # handle table with not auto fill
    if handleTableBasic or handleTableAdvance:
        if handleTableBasic:
            mask = detectTable(img).run(1)
        else:
            mask = detectTable(img).run(2)
        mask_img = mask
        ## resize
        listResult, listBigBox = getTableCoordinate(mask_img)
        # resize image ?
        img = cv2.resize(img, (mask_img.shape[1], mask_img.shape[0]))
        resultTable = GetText(listResult,listBigBox,img)
    return resultTable
import datetime
def saveResult(folder,saveFileName,result):
    file  = os.path.join(folder,saveFileName)
    if os.path.exists(file):
        f = open(file,"a+")
    else:
        f = open(file,"w+")
    f.write(result)
    f.close()
    print(str(datetime.datetime.now()) + " Scan successed")

def getFileName(fileType,folder):
    names = []
    if fileType == "pdf":
        count = 0
        for filename in os.listdir(folder):
            print(filename)
            if "pdf" in filename:
                filename = os.path.join(folder,filename)
                count = pdfToImage(filename,folder) ## convert to image
        for k in range(1,count+1):
            names.append(str(k)+".jpg")
    else:
        listname = os.listdir(folder)
        if fileType == "image":
            for name in listname:
                if name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    names.append(name)
        elif fileType == "text":
            for name in listname:
                if name.lower().endswith(('.txt', '.doc', '.docx')):
                    names.append(name)
    return names

def preprocessFile(fileType,folder,saveFileName,skew,blur,basic,advance):
    if skew.lower() == "true":
        skew = True
    else:
        skew = False
    if blur.lower() == "true":
        blur = True
    else:
        blur = False
    if basic.lower() == "true":
        basic = True
    else:
        basic = False
    if advance.lower() == "true":
        advance = True
    else:
        advance = False

    names = getFileName(fileType,folder)
    result = ""
    
    if "pdf" in fileType or "image" in fileType:
        for filename in names:
            filename = os.path.join(folder,filename)
            if ".jpg" in filename:
                resultTable = handleFile(filename,skew = skew,deblur=blur,handleTableBasic=basic,handleTableAdvance=advance)
                # k = 0
                for rs in resultTable:
                    # if k %4 == 0:
                    #     result = result + "\n"
                    result= result + (str(rs))
                    # k = k+ 1
                if fileType == "pdf":
                    os.remove(filename)
    elif fileType=="text":
        for filename in names:
            filename = os.path.join(folder,filename)
            f = open(filename,"r")
            result = result + str(f.read())
            f.close()
    if result != "":
        result = result.replace("'","")
        result = result.replace("\"","")
        saveResult(folder,saveFileName,result)
if __name__ == '__main__':
    # fileType = "pdf"## pdf, docx, jpg, txt
    # folderContainsFile = "./save/"
    # fileTextToSave = "text.txt"
    fileType,folderContainsFile,fileTextToSave,skew,blur,basic,advance = getInput()
    preprocessFile(fileType,folderContainsFile,fileTextToSave,skew,blur,basic,advance)
    # preprocessFile("pdf","./test","text.txt","false","false","true","false")

