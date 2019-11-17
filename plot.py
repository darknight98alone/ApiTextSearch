import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
import glob

files = glob.glob("*.jpg")
for file in files:

    img = cv2.imread(file,0)
    
    idx = (img.flatten()<5)
    temp = sum(idx[:])
    print(temp)
    if temp == 0:
        cv2.imshow("ok",img)
        cv2.waitKey(0)
    # hist,bins = np.histogram(img.flatten(),256,[0,256])

    # plt.hist(img.flatten(),256,[0,256], color = 'r')
    # plt.xlim([0,256])
    # plt.legend(('cdf','histogram'), loc = 'upper left')
    # plt.show()