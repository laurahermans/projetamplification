#from eulerian_magnify import eulerian_magnification, show_frequencies
#from pulse import get_pulse
#from pulse1 import get_pulse
from eulerian import eulerian_laplacian
import pickle
from eulerian import eulerian_magnification, get_pulse1, show_pulse, get_pulse, get_pulse2
from pulse import compte_pulse
from eulerian import  show_frequencies

from clique import mainc


import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2
import os


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("video_name", help="give the name of your video file which must be in the media folder. For example = media/nameofthevideo.mp4 ",
                    type=str)
parser.add_argument("pourcentage_largeur",help="give the % of the width of the interest zone. For example if the zone is at 75% from the left, you enter : 0.75",
                    type=float)
parser.add_argument("pourcentage_hauteur", help="give the % of the height of the interest zone. For example if the zone is at 75% from the bottom, you enter : 0.75",
                    type=float)
resultat = parser.parse_args()

nomvid=resultat.video_name
larg=resultat.pourcentage_largeur
long=resultat.pourcentage_hauteur



#show_frequencies('media/pap.mp4')
#eulerian_magnification('media/face.mp4', image_processing='gaussian', pyramid_levels=3, freq_min=50.0 / 60.0, freq_max=1.0, amplification=50)

#show_frequencies('media/baby.mp4')
#eulerian_magnification('media/face.mp4', image_processing='laplacian', pyramid_levels=5, freq_min=0.45, freq_max=1, amplification=50)

#get_pulse('media/video.mp4',0.5,0.5)
import time

#partie de code qui cree la video amplifiee et la stocke sous forme de liste dans un fichier txt

#video = eulerian_magnification('media/face.mp4', 0.5, 0.75, image_processing='gaussian', pyramid_levels=3, freq_min=50.0 / 60.0, freq_max=1.0, amplification=50)

#frame1, larg, haut = eulerian_laplacian(nomvid, larg, long, image_processing='laplacian', pyramid_levels=3, freq_min=0.5, freq_max=3.5, amplification=150)



video, frame1, larg, haut = eulerian_magnification(nomvid, larg, long, image_processing='laplacian', pyramid_levels=3, freq_min=0.801, freq_max=1.334, amplification=150)






listex, listey = mainc(frame1, larg, haut)

print listex
print listey
print listex[0]





#with open('file_listt.txt', 'wb') as f:
 #   pickle.dump(video, f)

# partie de code pour ouvrir le fichier contenant la liste et afficher la pulsation cardiaque

#with open('file_listt.txt', 'rb') as f:
 #   vid = pickle.load(f)
#debut_haut=vid[0]
#vid.remove(debut_haut)
#debut_large=vid[0]
#vid.remove(debut_large)
#pulse = get_pulse1(vid,debut_large,debut_haut)
#compte_pulse(pulse,29)
#show_pulse(pulse)


pulse = get_pulse2(video,listex,listey)
compte_pulse(pulse,29)
show_pulse(pulse)
