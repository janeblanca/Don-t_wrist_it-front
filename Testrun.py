import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
import numpy as np
from keras.models import load_model
import mediapipe as mp_mediapipe
import tensorflow as tf

class TimerApp(QMainWindow):
    def __init__(self):
        super(TimerApp, self).__init__()

        self.setGeometry(500, 500, 1200, 500)
        self.setWindowTitle("Computer Usage Timer")

        title_label = QtWidgets.QLabel("DON'T WRIST IT", self)
        title_label.setGeometry(10, 10, 1180, 30)
        title_label.setAlignment(QtCore.Qt.AlignLeft)
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)

        subtitle_label = QtWidgets.QLabel("Prevent Carpal Tunnel Syndrome", self)
        subtitle_label.setGeometry(10, 40, 1180, 30)
        subtitle_label.setAlignment(QtCore.Qt.AlignLeft)
        subtitle_font = subtitle_label.font()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)

        self.work_group_box = QGroupBox("Work Time", self)
        self.work_group_box.setGeometry(10, 80, 200, 70)
        self.work_layout = QVBoxLayout(self.work_group_box)
        self.work_label = QtWidgets.QLabel("00:00:00", self)
        self.work_layout.addWidget(self.work_label, alignment=QtCore.Qt.AlignLeft)

        self.break_group_box = QGroupBox("Break Time", self)
        self.break_group_box.setGeometry(220, 80, 200, 70)
        self.break_layout = QVBoxLayout(self.break_group_box)
        self.break_label = QtWidgets.QLabel("00:00:00", self)
        self.break_layout.addWidget(self.break_label, alignment=QtCore.Qt.AlignLeft)

        self.interval_group_box = QGroupBox("Break Interval", self)
        self.interval_group_box.setGeometry(430, 80, 200, 70)
        self.interval_layout = QVBoxLayout(self.interval_group_box)
        self.interval_label = QtWidgets.QLabel("00:00:00", self)
        self.interval_layout.addWidget(self.interval_label, alignment=QtCore.Qt.AlignLeft)

        self.camera_group_box = QGroupBox("Camera Setup", self)
        self.camera_group_box.setGeometry(640, 80, 530, 300)
        self.camera_layout = QVBoxLayout(self.camera_group_box)

        self.camera_label = QLabel(self)
        self.camera_label.setGeometry(650, 90, 510, 230)

        self.camera_dropdown = QComboBox(self)
        self.camera_dropdown.setGeometry(650, 330, 330, 30)
        self.camera_dropdown.addItem("Built-in Camera")
        self.camera_dropdown.currentIndexChanged.connect(self.select_camera)

        self.setup_button = QPushButton("Setup Camera", self)
        self.setup_button.setGeometry(990, 330, 170, 30)
        self.setup_button.clicked.connect(self.setup_camera)

        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_camera)

        self.work_timer = QTimer(self)
        self.break_timer = QTimer(self)
        self.interval_timer = QTimer(self)

        self.work_timer.timeout.connect(self.update_work_timer)
        self.break_timer.timeout.connect(self.update_break_timer)
        self.interval_timer.timeout.connect(self.update_interval_timer)

        self.work_elapsed_seconds = 0
        self.break_elapsed_seconds = 0
        self.interval_elapsed_seconds = 0

        # Load your modified machine learning model
        self.machine_learning_model = self.load_modified_model()

        self.camera_capture = None

        self.status_group_box = QGroupBox("Hand and Wrist Status", self)
        self.status_group_box.setGeometry(10, 400, 1160, 60)
        self.status_layout = QVBoxLayout(self.status_group_box)
        self.status_label = QtWidgets.QLabel("Status: Unknown", self)
        self.status_layout.addWidget(self.status_label, alignment=QtCore.Qt.AlignLeft)

        self.show()

    def load_modified_model(self):
        model_path = "C:/4th_yr/Project Design 1/GRU_model_4.h5"
        model = load_model(model_path)
        return model

    def update_work_timer(self):
        self.work_elapsed_seconds += 1
        self.update_displayed_time(self.work_elapsed_seconds, self.work_label)

    def update_break_timer(self):
        self.break_elapsed_seconds += 1
        self.update_displayed_time(self.break_elapsed_seconds, self.break_label)

    def update_interval_timer(self):
        self.interval_elapsed_seconds += 1
        self.update_displayed_time(self.interval_elapsed_seconds, self.interval_label)

    def update_displayed_time(self, elapsed_seconds, label):
        minutes, seconds = divmod(elapsed_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        label.setText(formatted_time)

    def preprocess_frame(self, frame):
        processed_frame = cv2.resize(frame, (126, 126))
        processed_frame = processed_frame[:, :, 0] / 255.0
        processed_frame = np.expand_dims(processed_frame, axis=0)
        processed_frame = np.expand_dims(processed_frame, axis=1)
        return processed_frame

    def setup_camera(self):
        selected_camera = self.camera_dropdown.currentText()

        if selected_camera == "Built-in Camera":
            self.camera_capture = cv2.VideoCapture(0)
        else:
            pass

        if self.camera_capture is not None and self.camera_capture.isOpened():
            self.camera_timer.start(30)
        else:
            print("Failed to open the camera.")

    def update_camera(self):
        if self.camera_capture is not None and self.camera_capture.isOpened():
            ret, frame = self.camera_capture.read()

            if ret:
                try:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    processed_frame = self.preprocess_frame(frame_rgb)

                    predictions = self.machine_learning_model.predict(processed_frame)

                    height, width, channel = frame_rgb.shape
                    bytes_per_line = 3 * width
                    q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)

                    self.camera_label.clear()
                    self.camera_label.setPixmap(pixmap)

                    if predictions[0] == 0:
                        self.status_label.setText("Status: Correct Position")
                    else:
                        self.status_label.setText("Status: Wrong Position")
                except Exception as e:
                    print(f"Error during prediction: {e}")
            else:
                print("Failed to read frame from the camera.")
        else:
            print("Camera not initialized or not opened.")

    def select_camera(self, index):
        selected_camera = self.camera_dropdown.currentText()
        print(f"Selected Camera: {selected_camera}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer_app = TimerApp()
    timer_app.work_timer.start(1000)
    timer_app.break_timer.start(1000)
    timer_app.interval_timer.start(1000)
    sys.exit(app.exec_())
