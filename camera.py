from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QImage, QPixmap  # Add QImage and QPixmap
from PyQt5.QtCore import Qt, QRect
import sys
# import cv2

from feature_extraction import HandLandmarksDetector

class Camera(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.detector = HandLandmarksDetector()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Camera Stream')
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.white, 0.5))
        color = QColor("#3A606E")
        color.setAlpha(100)
        painter.setBrush(color)
        camera_square = QRect(self.width() - 420, 330, 390, 350)
        radius = 7
        painter.drawRoundedRect(camera_square, radius, radius)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera = Camera()
    sys.exit(app.exec_())
