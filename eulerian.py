import cv2
import os
import sys

import numpy
import pylab
import scipy.signal
import scipy.fftpack

import cv2.cv as cv



def eulerian_magnification(video_filename, pour_larg, pour_haut, image_processing='gaussian', freq_min=0.833, freq_max=1, amplification=50, pyramid_levels=4):
    """Amplify subtle variation in a video and save it to disk"""
    path_to_video = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), video_filename)
    orig_vid, fps, larg, haut, frame1 = load_video(path_to_video)
#    print "fps = " + str(fps)
    pulse = []
    if image_processing == 'gaussian':
        vid_data = gaussian_video(orig_vid, pyramid_levels)
        print vid_data.shape
    elif image_processing == 'laplacian':
        vid_data = laplacian_video(orig_vid, pyramid_levels)
    vid_data = temporal_bandpass_filter(vid_data, fps, freq_min=freq_min, freq_max=freq_max)
    print "Amplifying signal by factor of " + str(amplification)
    vid_data *= amplification
    file_name = os.path.splitext(path_to_video)[0]
    file_name = file_name + "_min"+str(freq_min)+"_max"+str(freq_max)+"_amp"+str(amplification)
    video = combine_pyramid_and_save(vid_data, orig_vid, pyramid_levels, fps, save_filename=file_name + '_magnified.mp4')
#    debut_larg = int(pour_larg*larg)
#    debut_haut = int(pour_haut*haut)
#    video.insert(0,debut_larg)
#    video.insert(0,debut_haut)
    path = os.path.dirname(os.path.realpath(__file__))+'/'
    os.chdir(path)
    cv2.imwrite('media/test1.png', frame1)
    frame = 'media/test1.png'
    return video, frame, larg, haut





def show_pulse(pulse):
    charts_x = 1
    charts_y = 2
    pylab.figure(figsize=(charts_y, charts_x))
    pylab.subplot(charts_y, charts_x, 1)
    pylab.title("Pulse")
    pylab.plot(pulse)
    pylab.show()

def get_pulse(video_filename):
    path_to_video = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), video_filename)
    orig_vid, fps = load_video(path_to_video)
    pulse = []
    print orig_vid.shape
    print fps
    pulse = []
    for i in range(0,orig_vid.shape[0]):
        pulse.append(get_pixel(orig_vid[i]))
    return pulse

def get_pulse1(video,debut_large,debut_haut):
    pulse = []
    for i in range(0,len(video)):
        pulse.append(get_pixel(video[i],debut_large,debut_haut))
    return pulse

def get_pulse2(video,listex,listey):
    pulse = []
    for i in range(0,len(video)):
        pulse.append(get_pixel1(video[i],listex,listey))
    return pulse

def show_frequencies(video_filename, bounds=None):
    """Graph the average value of the video as well as the frequency strength"""
    original_video, fps, larg, haut, frame2 = load_video(video_filename)
    print fps
    averages = []

    if bounds:
        for x in range(1, original_video.shape[0] - 1):
            averages.append(original_video[x, bounds[2]:bounds[3], bounds[0]:bounds[1], :].sum())
    else:
        for x in range(1, original_video.shape[0] - 1):
            averages.append(original_video[x, :, :, :].sum())

    charts_x = 1
    charts_y = 2
    pylab.figure(figsize=(charts_y, charts_x))
    pylab.subplots_adjust(hspace=.7)

    pylab.subplot(charts_y, charts_x, 1)
    pylab.title("Pixel Average")
    pylab.plot(averages)

    frequencies = scipy.fftpack.fftfreq(len(averages), d=1.0 / fps)

    pylab.subplot(charts_y, charts_x, 2)
    pylab.title("FFT")
    pylab.axis([0, 15, -4000000, 10000000])
    pylab.plot(frequencies, scipy.fftpack.fft(averages))

    pylab.show()


def temporal_bandpass_filter(data, fps, freq_min=0.833, freq_max=1.333, axis=0):
    print "Applying bandpass between " + str(freq_min) + " and " + str(freq_max) + " Hz"
    fft = scipy.fftpack.fft(data, axis=axis)
    frequencies = scipy.fftpack.fftfreq(data.shape[0], d=1.0 / fps)
    bound_low = (numpy.abs(frequencies - freq_min)).argmin()
#    print "bl" + str(bound_low)
    bound_high = (numpy.abs(frequencies - freq_max)).argmin()
#    print "bh" + str(bound_high)
    fft[:bound_low] = 0
    fft[bound_high:-bound_high] = 0
    fft[-bound_low:] = 0
    return scipy.fftpack.ifft(fft, axis=0)





def load_video(video_filename):
    """Load a video into a numpy array"""
    print "Loading " + video_filename
    # noinspection PyArgumentList
    capture = cv2.VideoCapture(video_filename)
    frame_count = int(capture.get(cv.CV_CAP_PROP_FRAME_COUNT))
    print frame_count
    width, height = get_capture_dimensions(capture)
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
    frame1 = orig_vid[1]

    capture.release()
    return orig_vid, fps, width, height, frame1


def save_video(video, fps, save_filename='media/output.avi'):
    """Save a video to disk"""
    fourcc = cv.CV_FOURCC('M', 'J', 'P', 'G')
    writer = cv2.VideoWriter(save_filename, fourcc, fps, (video.shape[2], video.shape[1]), 1)
    for x in range(0, video.shape[0]):
        res = cv2.convertScaleAbs(video[x])
        writer.write(res)


def gaussian_video(video, shrink_multiple):
    """Create a gaussian representation of a video"""
    vid_data = None
    for x in range(0, video.shape[0]):
        frame = video[x]
        gauss_copy = numpy.ndarray(shape=frame.shape, dtype="float")
        gauss_copy[:] = frame
        for i in range(shrink_multiple):
            gauss_copy = cv2.pyrDown(gauss_copy)
        if x == 0:
            vid_data = numpy.zeros((video.shape[0], gauss_copy.shape[0], gauss_copy.shape[1], 3))
        vid_data[x] = gauss_copy
    return vid_data


def laplacian_video(video, shrink_multiple):
    vid_data = None
    for x in range(0, video.shape[0]):
        frame = video[x]
        gauss_copy = numpy.ndarray(shape=frame.shape, dtype="float")
        gauss_copy[:] = frame
        for i in range(shrink_multiple):
            prev_copy = gauss_copy[:]
            gauss_copy = cv2.pyrDown(gauss_copy)

        laplacian = prev_copy - cv2.pyrUp(gauss_copy)
        if x == 0:
            vid_data = numpy.zeros((video.shape[0], laplacian.shape[0], laplacian.shape[1], 3))
        vid_data[x] = laplacian
    return vid_data


def combine_pyramid_and_save(g_video, orig_video, enlarge_multiple, fps, save_filename='media/output.mp4'):
    """Combine a gaussian video representation with the original and save to file"""
    width, height = get_frame_dimensions(orig_video[0])
    fourcc = cv.CV_FOURCC('m', 'p', '4', 'v')
#    writer = cv2.VideoWriter(save_filename, fourcc, fps, (width, height), 1)
    writer = cv2.VideoWriter()
#    pulse = []
    video = []
    print writer.open(save_filename, fourcc, fps, (width, height), True)
    for x in range(0, g_video.shape[0]):
        img = numpy.ndarray(shape=g_video[x].shape, dtype='float')
        img[:] = g_video[x].imag
        for i in range(enlarge_multiple):
            img = cv2.pyrUp(img)
        img[:height, :width] = img[:height, :width] + orig_video[x]
#        pulse.append(get_pixel(img[:]))
        video.append(img[:])
        res = cv2.convertScaleAbs(img[:height, :width])
        writer.write(res)
    writer.release()
    return video
    writer=None

def get_pixel(frame,debut_large, debut_haut):
    pixtot=0
    a=0
    debhaut = debut_haut-5
    finhaut = debut_haut+5
    deblarg = debut_large-5
    finlarg = debut_large+5
    for x in range(debhaut,finhaut):
        for y in range(deblarg,finlarg):
            pixtot = pixtot + frame[x,y,0]
            a=a+1
    pixtot = pixtot/a
    return pixtot


def get_pixel1(frame,listex, listey):
    pixtot=0
    a=0
    debg = listex[0]
    fing = listex[1]
    debh = listey[0]
    finh = listey[1]
    for x in range(debg,fing):
        for y in range(debh,finh):
            pixtot = pixtot + frame[y,x,0]
            a=a+1
    pixtot = pixtot/a
    return pixtot



def get_capture_dimensions(capture):
    """Get the dimensions of a capture"""
    width = int(capture.get(cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
    return width, height


def get_frame_dimensions(frame):
    """Get the dimensions of a single frame"""
    height, width = frame.shape[:2]
    return width, height


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = scipy.signal.butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = scipy.signal.lfilter(b, a, data, axis=0)
    return y




