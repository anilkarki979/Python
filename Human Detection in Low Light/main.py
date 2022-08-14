from tkinter import *
from tkinter import filedialog
import os
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np


def showimage():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("JPG File","*.jpg"),("PNG file","*.png"),("All files","*.*")))
    os.system("python detect.py --conf 0.5 --source " + filename)


def playvideo():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Video File", filetypes=(("MP4 File","*.mp4"),("AVI file","*.avi"),("All files","*.*")))
    os.system("python detect.py --conf 0.5 --save-crop --name output --source " + filename)

def cam():
    os.system("python detect.py --conf 0.5 --save-crop --name output --source 0 ")


def StartCam():
    net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
    classes = []
    with open('coco.names', 'r') as f:
        classes = f.read().splitlines()
    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()
        height, width, _ = img.shape

        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)

        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)

        # print(len(boxes))
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        # print(indexes.flatten())
        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(len(boxes), 3))

        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i], 2))
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label + " " + confidence, (x, y - 10), font, 2, (255, 255, 255), 2)

        cv2.imshow('Image', img)
        key = cv2.waitKey(1)
        if key == 32:
            break

    cap.release()
    cv2.destroyAllWindows()


def enhance():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(
    ("JPG File", "*.jpg"), ("PNG file", "*.png"), ("All files", "*.*")))
    os.system("python enhance.py  " )




#root = Tk()
root = tk.Tk()


text = Label(root, text='Human Detection in Low Light ', font=16 , height=5, width=30)
text.pack(side=TOP,padx=15, pady=5)

frm = Frame(root)
frm.pack(side=BOTTOM, padx=15, pady=15)

lbl = Label(root)
lbl.pack()

btn = Button(frm, text="Browse Image", command=showimage)
btn.pack(side=tk.LEFT)

btn = Button(frm, text="Browse Video", command=playvideo)
btn.pack(side=tk.LEFT,padx=10)

btn = Button(frm, text="Start Camera", command=cam)
btn.pack(side=tk.LEFT,padx=20)

btn = Button(frm, text="Enhancement", command=enhance)
btn.pack(side=tk.LEFT,padx=30)

btn2 = Button(frm, text="Exit", command=lambda: exit())
btn2.pack(side=tk.LEFT,padx=30)

root.title("Detection")
root.geometry("700x250")
root.mainloop()