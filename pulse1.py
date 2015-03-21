import cv2
import os
import sys

import numpy
import pylab
import scipy.signal
import scipy.fftpack

import cv2.cv as cv

def get_pulse(video_filename):
    path_to_video = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), video_filename)
    orig_vid, fps = load_video(path_to_video)
    pulse = []
    print orig_vid.shape
    print fps
    pulse = []
    for i in range(0,orig_vid.shape[0]):
        pulse.append(get_pixel(orig_vid[i]))
    show_pulse(pulse)



def show_pulse(pulse):
    charts_x = 1
    charts_y = 2
    pylab.figure(figsize=(charts_y, charts_x))
    pylab.subplot(charts_y, charts_x, 1)
    pylab.title("Pulse")
    pylab.plot(pulse)
    pylab.show()


def get_pixel(frame):
    pixtot=0
    a=0
    for x in range(463,483):
        for y in range(254,274):
            pixtot = pixtot + frame[x,y,0]
            a=a+1
    pixtot = pixtot/a
    return pixtot


def load_video(video_filename):
    """Load a video into a numpy array"""
    print "Loading " + video_filename
    # noinspection PyArgumentList
    capture = cv2.VideoCapture(video_filename)
    frame_count = int(capture.get(cv.CV_CAP_PROP_FRAME_COUNT))
    width, height = get_capture_dimensions(capture)
    print width
    print height
    rgb=[]
    fps = int(capture.get(cv.CV_CAP_PROP_FPS))
    x = 0
    orig_vid = numpy.zeros((frame_count, height, width, 3), dtype='uint8')
    rgb = capture.get(cv.CV_CAP_PROP_CONVERT_RGB)
    print rgb
    while True:
        _, frame = capture.read()
        if frame is None or x >= frame_count:
            break
        orig_vid[x] = frame
        x += 1
    capture.release()
    return orig_vid, fps

def get_capture_dimensions(capture):
    """Get the dimensions of a capture"""
    width = int(capture.get(cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
    return width, height
