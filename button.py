import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class PicButton(QtWidgets.QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
layout = QtWidgets.QHBoxLayout(window)

button = PicButton(QtGui.QPixmap("icons/arrow-left-solid-white-back.png"))
layout.addWidget(button)

window.show()
sys.exit(app.exec_())
