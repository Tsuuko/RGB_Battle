# -*- coding:utf-8 -*-
# pylint: disable=E1101

import cv2, matplotlib
import numpy as np
import matplotlib.pyplot as plt
import base64
from PIL import Image
import io
import sys

#ローカルにあるファイルから読み込み。テスト用
DEBUG=True

def encodeImage(filename):
    """
    画像ファイルをbase64にエンコード。

    filename : str

    """

    with open(filename, "rb") as f:
        base64_image = base64.b64encode(f.read())

    return base64_image

def decodeImage(base64_image):
    """
    base64でエンコードされた画像をデコード

    base64_image : str
    """

    binary_image=base64.b64decode(base64_image)

    return binary_image
def showImage(img):
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def loadImageByBinary(binary_image):
    """
    デコード後のバイナリファイルをopenCVに読み込み。

    binary_image : bytes
    """
    size=(800,800)
    arr = np.asarray(bytearray(binary_image), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    img=cv2.resize(img, size)
    gray_img = cv2.imdecode(arr, 0)
    gray_img=cv2.resize(gray_img, size)
    canny_img = cv2.Canny(gray_img, 120, 100)



    #size=(800,800)
    #arr = np.asarray(bytearray(binary_image), dtype=np.uint8)
    #img = cv2.imdecode(arr, -1)
    #img=cv2.resize(img, size)
    #gray_img = cv2.imdecode(arr, 0)
    #gray_img=cv2.resize(gray_img, size)
    #canny_img = cv2.Canny(gray_img, 120, 100)
    #showImage(img)

    return img,gray_img,canny_img

def calcRGB(img):
    """
    引数に指定した画像の平均RGB値を算出、
    最大の色を文字列"R","G","B"で返す。

    img : numpy.ndarray
    """

    average_color_row=np.mean(img,axis=0)
    average_color=np.mean(average_color_row,axis=0)
    max_index=np.argmax(average_color)
    #print(average_color)


    if max_index==0:
        return "B",average_color
    elif max_index==1:
        return "G",average_color
    else:
        return "R",average_color

def calcEdge(canny_img):

    count_edge_row=np.sum(canny_img==255)#,axis=0)

    return count_edge_row

def calcBP(average_color,edge_count):
    color_score=(average_color[np.argmax(average_color)]/sum(average_color)*100)
    edgescore=(edge_count/640000*100)
    BP=int(edgescore*color_score*10)

    return BP

def run(image):
    #filename="img.jpg"
    img,gray_img,canny_img=loadImageByBinary(image)
    #showImage(img)
    color,average_color=calcRGB(img)
    edge_count=calcEdge(canny_img)
    BP=calcBP(average_color,edge_count)

    return color,BP

if __name__ == "__main__":
    if DEBUG==True:
        filename="img.jpg"
        base64_string=encodeImage(filename)
    else:
        #第2引数をbase64_stringに格納（第一引数はpyファイル）
        base64_string=sys.argv[1]

    #画像をbase64からバイナリ形式にデコード
    binary_image=decodeImage(base64_string)

    #OpenCVに読み込ませる
    img,gray_img,canny_img=loadImageByBinary(binary_image)
    #最大の色を計算
    color,average_color=calcRGB(img)

    #showImage(img)
    #showImage(gray_img)
    edge_count=calcEdge(canny_img)
    BP=calcBP(average_color,edge_count)

    if DEBUG==True:
        print("結果："+color,BP)
