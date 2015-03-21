import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

liste_posx = []
liste_posy = []
posx = 0
posy = 0

app = QtGui.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

class Example(QtGui.QWidget):





    def __init__(self, frame1, larg, haut):
        super(Example, self).__init__()

        self.initUI(frame1, larg, haut)

    def mousePressEvent(self, QMouseEvent):
        posx = QMouseEvent.pos().x()
        posy = QMouseEvent.pos().y()
        liste_posx.append(posx)
        liste_posy.append(posy)
       # print liste_posx
        #print QMouseEvent.pos()


    def mouseReleaseEvent(self, QMouseEvent):
        cursor =QtGui.QCursor()
        #print cursor.pos()



    def initUI(self, frame1, larg, haut):

        qbtn = QtGui.QPushButton('Quit', self)
        #qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.clicked.connect(self.test)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)

        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        path = os.path.dirname(os.path.realpath(__file__))+'/'
        os.chdir(path)
        palette	= QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap(frame1)))

        self.setPalette(palette)



        self.setGeometry(0, 0, larg, haut)
        self.setWindowTitle('Essai')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        #self.connect("clicked", self.test)
       # self.connect(qbtn, QtCore.SIGNAL("clicked()"), self.click)
        self.show()

    def getPos(self , event):
        x = event.pos().x()
        y = event.pos().y()

    def test(self):
        self.close()
        self.setParent(None)
        closeQt()

def closeQt():
    app.quit()





   # def click(self):
        #qbtn.setText("Clique !")


def mainc(frame1, larg, haut):

    ex = Example(frame1, larg, haut)
    app.exec_()
    return liste_posx, liste_posy




