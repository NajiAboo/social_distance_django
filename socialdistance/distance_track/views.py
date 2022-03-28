"""
    This module is to capture the video and return the frame after processing
    If human in the frame are too close they will mareked as in red color
"""
import threading
import cv2
import logging
from distance_track.detect import Detect
from distance_track.distancewatcher import DistanceWatcher

from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse

logger = logging.getLogger(__name__)


@gzip.gzip_page
def home(request):

    """
    Home view to reuturn the video frames
    """
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except IOError as error:
        logger.error(error)
    return render(request, 'distance_track/app.html')


class VideoCamera(object):
    """
    Purpose of this class is to capture the video and modify the frame based on the detected 
    human and its distance
    """
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.detect = Detect()
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        """
          Used to get the frame
        """
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)


        df_human = self.detect.detect_human(self.frame)
        if len(df_human) > 1:
            watcher = DistanceWatcher(df_human, self.frame)
            jpeg = watcher.process_frame()
            _, jpeg = cv2.imencode('.jpg', jpeg)

        return jpeg.tobytes()

    def update(self):
        """
            update the frame
        """
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    """"
        Get the frame from the camera
    """
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')