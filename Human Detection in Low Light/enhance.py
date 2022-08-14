from PIL import Image, ImageEnhance,ImageOps
import cv2
from glob import glob

img_path=glob("C:\\Users\\HP\\Desktop\\P\\Project\\yolov5-master\\yolov5-master\\runs\\detect\\output8\\crops\\human\\*.jpg") #cropped img ko location deu with extension

for im in img_path:
    im0=Image.open(im)
    # im0=PIL.ImageOps.autocontrast(im0)
    im0=ImageEnhance.Color(im0).enhance(1.5)
    im0=ImageEnhance.Brightness(im0).enhance(3)
    im0=ImageEnhance.Contrast(im0).enhance(0.8)
    im0=ImageEnhance.Sharpness(im0).enhance(1.9)
    im0.save("C:\\Users\\HP\\Desktop\\P\\Project\\yolov5-master\\yolov5-master\\runs\\detect\\output8\\crops\\human\\"+im.split('\\')[-1])
   # print("\\content\\gdrive\\MyDrive\\output\\"+im.split('\\')[-1])