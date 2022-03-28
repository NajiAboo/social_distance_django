"""
    This module Watch the distance
"""
import math
from itertools import combinations

import cv2

class DistanceWatcher:
    """
     Distance Watcher watches the distance between the perons
    """
    def __init__(self,df_human, frame) -> None:
        self.df_human = df_human
        self.frame = frame
        
        self.centroid_dict ={}
        self.red_zone_list = []
        self.red_line_list = []

    def is_close(self,p1,p2):
        """ Function check how close the person"""
        dist = math.sqrt(p1**2+ p2**2)
        
        #dist = math.dist(p1,p2)
        
        return dist

    def prepare_centroid(self):
        """
         Calculate the centroid of the images
        """
        objectid = 0

        for index,detections in self.df_human.iterrows():
            xmin,ymin,xmax,ymax = detections["xmin"],detections["ymin"],detections["xmax"],detections["ymax"]
            x,y = (xmin+xmax)/2, (ymin+ymax)/2
            self.centroid_dict[objectid]  =(int(x), int(y), xmin,ymin,xmax,ymax)
            objectid+=1

    def check_red_green_zone(self):
        """
         Calculate the images are red or green
        """

        for (id1, p1), (id2,p2) in combinations(self.centroid_dict.items(),2):
 
            dx,dy = p1[0]-p2[0],p1[1]-p2[1]
            distance = self.is_close(dx,dy)
            print("distance")
            print(dx,dy)
            print(distance)

        if distance < 300.0:
            if id1 not in self.red_zone_list:
                self.red_zone_list.append(id1)
                self.red_line_list.append(p1[0:2])
            if id2 not in self.red_zone_list:
                self.red_zone_list.append(id2)
                self.red_line_list.append(p2[0:2])

    def manipulate_frame(self):
        """
         Manipulate the frame. checks the box
        """
        for idx,box in self.centroid_dict.items():
            if idx in self.red_zone_list:
                c1 = box[2],box[3]
                c2 = box[4],box[5]
                cv2.rectangle(self.frame, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])),(0,0,255), 2)
               
            else:
                c1 = box[2],box[3]
                c2 = box[4],box[5]
                cv2.rectangle(self.frame, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])), (0, 255, 0), 2)


    def process_frame(self):
        """
          Process the frame
        """
        
        self.prepare_centroid()
        self.check_red_green_zone()
        self.manipulate_frame()

        return self.frame

