"""
  Detect the image
"""
import cv2
import numpy as np
import torch
from PIL import Image
from django.core.files.storage import default_storage

from socialdistance import settings

import os

 

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
 

class Detect:
    
    def __init__(self) -> None:
        pass

    def detect_human(self,img):
      """
      Detect the frame human
      """
      
      #  img = np.array(img)
      fname = settings.MEDIA_ROOT+"/temp.jpeg"
      cv2.imwrite(fname, img)
      #im.save("test.jpg")
      #default_storage.save("test.jpeg",im)
      results = model(fname)
      print(results)
      df = results.pandas().xyxy[0]
      filter = df["name"]=="person"
      df = df.loc[filter]
      return df