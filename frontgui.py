import sys
from PyQt5.QtWidgets import QApplication, QWidget,  QLineEdit, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QIntValidator
from PyQt5.QtCore import Qt, QRect
from plyer import notification
import cv2

from camera import Camera
from cam_permission import CamPermission
from break_time import Break
from audio import Audio
from worktime import Worktime
from breaktime import Breaktime
from breakinterval import BreakInterval
from wristposition import WristPosition
from reminder import Reminder
from gtts import gTTS
import os

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the UI components
        self.init_ui()

        # Disable maximized window
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        #  Camera
        self.show_camera = False
        self.camera = Camera(self)
        self.timer = self.startTimer(1000)


        # Break
        self.break_handler = Break(self)

        # Audio
        self.audio = Audio(self)

        # Worktime
        self.worktime = Worktime(self)

        # Breaktime
        self.breaktime = Breaktime(self)

        # BreakInterval
        self.breakinterval = BreakInterval(self)

        # WristPosition
        self.wristposition= WristPosition(self)

        # Reminder
        self.reminder = Reminder(self)

        # Break Time Input
        self.user_input_break = QLineEdit(self)
        self.user_input_break.setGeometry(355, 195, 50, 30)
        self.user_input_break.setStyleSheet("background-color: #f3f1ec; border: none; color: #303030; font-size: 14px;")
        self.user_input_break.setValidator(QIntValidator())

        # Break Interval Input
        self.user_input_interval = QLineEdit(self)
        self.user_input_interval.setGeometry(565, 195, 50, 30)
        self.user_input_interval.setStyleSheet(
            "background-color: #f3f1ec; border: none; color: #303030; font-size: 14px;")
        self.user_input_interval.setValidator(QIntValidator())

        self.user_input_break.returnPressed.connect(self.validate_inputs)
        self.user_input_interval.returnPressed.connect(self.validate_inputs)

        self.break_time = 0
        self.break_interval = 0
        self.original_break_time = 0
        self.original_break_interval = 0
        self.total_break_interval = 0
        self.total_work_time = 0
        self.break_interval_active = False
        self.initial_run = True

        self.set_break_interval()
        self.start_timer()


    def init_ui(self):
        self.setWindowTitle("Don't Wrist It")
        self.setStyleSheet("background-color: #f3f1ec;")
        self.setFixedSize(1200, 720)  # fixed size

    def paintEvent(self, event):
        painter = QPainter(self)

        # LEFT PANE
        pen = QPen(QColor("#e8e7e7"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#e8e7e7"))
        painter.drawRect(0, 0, 80, self.height())

        # CAMERA PANE
        painter.setBrush(QColor("#828E82"))
        painter.drawRect(self.width() - 450, 0, 450, self.height())

        # Display Total Work Time
        font_counter = QFont()
        font_counter.setPointSize(10)
        painter.setFont(font_counter)
        painter.setPen(QColor("#303030"))
        painter.drawText(140, 200, 150, 30, Qt.AlignLeft, "Time Work Time:")
        painter.drawText(180, 240, 150, 30, Qt.AlignLeft, f"{self.format_time(self.total_work_time)}")

        # Display Break Time Counter
        font_counter = QFont()
        font_counter.setPointSize(10)
        painter.setFont(font_counter)
        painter.setPen(QColor("#303030"))
        painter.drawText(333, 240, 150, 30, Qt.AlignLeft, f"Time left: {self.format_time(self.break_time)}")

        # Display Break Interval Counter
        font_counter.setPointSize(10)  # Set a smaller font size
        painter.setFont(font_counter)
        painter.setPen(QColor("#303030"))
        painter.drawText(545, 240, 150, 30, Qt.AlignLeft, f"Interval left: {self.format_time(self.break_interval)}")

        # ------------TEXTS----------
        # Don't Wrist It (Dashboard)
        font_title = QFont()
        font_title.setPointSize(14)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(105, 38, 450, 270, Qt.AlignLeft, "DON'T WRIST IT")

        # Tagline
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#6A6969"))
        painter.drawText(105, 71, 450, 270, Qt.AlignLeft, "Prevent Carpal Tunnel Syndrome")


        # Don't Wrist It (Logo)
        font_title2 = QFont()
        font_title2.setPointSize(13)
        painter.setFont(font_title2)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(self.width() - 450, 100, 450, 270, Qt.AlignCenter, "DON'T WRIST IT")

        # Setting-up Camera
        font_desc = QFont()
        font_desc.setPointSize(10)
        painter.setFont(font_desc)
        painter.drawText(self.width() - 430, 305, 450, self.height(), Qt.AlignLeft, "Setting-up your Camera")


        # Camera
        self.camera.cam_container(painter)
        if self.camera.cam_placeholder:
            self.camera.cam_holder(painter)
        else:
            self.camera.cam_draw(painter)

        # Audio
        self.audio.audio_container(painter)
        self.audio.audio_holder(painter)

        # Worktime
        self.worktime.worktime_container(painter)
        self.worktime.worktime_holder(painter)

        # Breaktime
        self.breaktime.breaktime_container(painter)
        self.breaktime.breaktime_holder(painter)

        # BreakInterval
        self.breakinterval.breakinterval_container(painter)
        self.breakinterval.breakinterval_holder(painter)

        # WristPosition
        self.wristposition.wristposition_container(painter)
        self.wristposition.wristposition_holder(painter)

        # Reminder
        self.reminder.reminder_container(painter)
        self.reminder.reminder_holder(painter)

        #------------IMAGES----------
        # image LOGO
        image_logo = QPixmap("./src/logo.png")
        image_logo_x = self.width() - 450 + (450 - image_logo.width()) // 2
        painter.drawPixmap(image_logo_x, -70, image_logo.width(), image_logo.height(), image_logo)



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()
            camera_container = QRect(self.width() - 420, 330, 390, 350)
            if camera_container.contains(click_pos):
                # Call CamPermission class to display Message Box
                message_box = CamPermission()
                result = message_box.exec_()
                # Click "Allow" or "Don't Allow"
                if result == QMessageBox.Yes:
                    print("Camera access allowed")
                    self.camera.cam_placeholder = False
                    self.update()
                else:
                    self.camera.cam_placeholder = True
                    print("Camera access denied.")

            audio_pane = QRect(105, self.height() - 115, self.width() - 577, 85)
            if audio_pane.contains(click_pos):
                # Clicked on the audio_pane, play audio
                self.audio.speak_text()

        super().mousePressEvent(event)

    def timerEvent(self, event):
        if event.timerId() == self.timer:
            self.camera.update()

            if self.break_interval_active:
                if self.break_interval > 0:
                    self.break_interval -= 1

                    if self.break_interval == 0:
                        self.break_interval_active = False
                        self.break_time = self.original_break_time
                        self.show_notification("Take a Break!", "Do Wrist Exercises!")

            else:
                if self.break_time > 0:
                    self.break_time -= 1

                    if self.break_time == 0:
                        self.break_interval_active = True
                        self.total_work_time += self.original_break_interval  # Add to total work time
                        self.break_interval = self.original_break_interval
                        self.show_notification("Break Time Over", "Back to work!")

            self.update()

    def closeEvent(self, event):
        self.camera.release_camera()
        event.accept()

    def set_break_time(self):
        self.break_handler.set_break_time()

    def set_break_interval(self):
        self.break_handler.set_break_interval()

    def format_time(self, seconds):
        return self.break_handler.format_time(seconds)

    def validate_inputs(self):
        self.break_handler.validate_inputs()

    def start_timer(self):
        self.break_handler.start_timer()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())