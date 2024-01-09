from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QRect
import cv2
import numpy as np
from feature_extraction import HandLandmarksDetector


class Camera:
    def __init__(self, parent):
        self.parent = parent
        self.camera = cv2.VideoCapture(0)
        self.cam_placeholder = True

    def cam_container(self, painter):
        painter.setPen(QPen(Qt.white, 0.5))
        color = QColor("#3A606E")
        color.setAlpha(100)
        painter.setBrush(color)
        camera_square = QRect(self.parent.width() - 420, 330, 390, 350)
        radius = 7
        painter.drawRoundedRect(camera_square, radius, radius)

    def cam_draw(self, painter):
        ret, frame = self.camera.read()
        if ret:
            # MediaPipe
            landmarks_detector = HandLandmarksDetector()
            frame_with_landmarks = landmarks_detector.draw_landmarks(frame)
            landmarks = landmarks_detector.extract_landmarks(frame)

            print(landmarks)

            # Reshaping the extracted landmarks to fit into the model
            landmarks_arr = np.array(landmarks)
            reshaped_landmarks = landmarks_arr.reshape((1, 1, landmarks_arr.shape[0]))

            # Display in the desktop application
            frame_with_landmarks = cv2.cvtColor(frame_with_landmarks, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            landmarks_image = QImage(frame_with_landmarks.data, w, h, bytes_per_line, QImage.Format_RGB888)
            dest_rect = QRect(790, 370, 370, 270)
            painter.drawImage(dest_rect, landmarks_image.scaled(dest_rect.size(), Qt.KeepAspectRatio))

    def cam_holder(self, painter):
        image_cam = QPixmap("./src/cam.png")
        image_cam_rect = QRect(self.parent.width() - 380, 380, 300, 210)
        painter.drawPixmap(image_cam_rect, image_cam)
        click_font = QFont()
        click_font.setPointSize(9)
        painter.setFont(click_font)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(self.parent.width() - 445, 480, 450, 270, Qt.AlignCenter, "Click to set-up your camera")

    def update(self):
        self.parent.update()

    def release_camera(self):
        self.camera.release()
