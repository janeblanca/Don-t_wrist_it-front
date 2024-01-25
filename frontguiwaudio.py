import sys
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QApplication, QWidget,  QLineEdit, QMessageBox, QScrollArea, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QIntValidator, QImage
from PyQt5.QtCore import Qt, QRect, QThread, pyqtSignal
from plyer import notification
from feature_extraction import HandLandmarksDetector
import cv2
import numpy as np

from camera import Camera
from cam_permission import CamPermission
from break_time import Break
from audio import Audio
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

        # Store Notification message
        self.notification_message = ""
        self.notification_container = False
        self.notifications = []

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


        # WORKTIME
        painter.setBrush(QColor("#FFFFFF"))
        # worktime = QRect(105, self.height() - 600, self.width() - 1000, self.height() - 520)
        worktime = QRect(105, 115, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(worktime, radius, radius)


        # small square ICON (Green Clock)
        painter.setBrush(QColor("#D0FFCF"))
        square_green_box = QRect(119, self.height() - 593, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_green_box, radius, radius)

        # small square (Worktime)
        painter.setBrush(QColor("#D0FFCF"))
        square_green_box = QRect(185, self.height() - 583, 105, 30)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_green_box, radius, radius)

        # BREAKTIME
        painter.setBrush(QColor("#FFFFFF"))
        breaktime = QRect(317, 115, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(breaktime, radius, radius)

        # small square ICON (BLue Clock)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(329, self.height() - 593, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)

        # small square (Breaktime)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(395, self.height() - 583, 105, 30)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)

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

        # BREAk INTERVAL
        pen = QPen(QColor("#FFFFFF"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#FFFFFF"))
        breakinterval = QRect(529, 115, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(breakinterval, radius, radius)

        # small square ICON (Yellow Clock)
        painter.setBrush(QColor("#FFF7AE"))
        square_yellow_box = QRect(540, self.height() - 593, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_yellow_box, radius, radius)

        # small square(Break Interval)
        painter.setBrush(QColor("#FFF7AE"))
        square_yellow_box = QRect(607, self.height() - 583, 105, 30)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_yellow_box, radius, radius)

        # Display Break Interval Counter
        font_counter.setPointSize(10)  # Set a smaller font size
        painter.setFont(font_counter)
        painter.setPen(QColor("#303030"))
        painter.drawText(545, 240, 150, 30, Qt.AlignLeft, f"Interval left: {self.format_time(self.break_interval)}")

        # WRIST POSITION
        pen = QPen(QColor("#FFFFFF"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#FFFFFF"))
        wristposition = QRect(105, 360, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(wristposition, radius, radius)

        # Reminder
        pen = QPen(QColor("#FFFFFF"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#FFFFFF"))
        reminder = QRect(317, 360, self.width() - 788, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(reminder, radius, radius)

        # small square ICON (Wrist Position)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(119, self.height() - 347, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)

        # small square (Correct - Wrist Position)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(183, 382, 105, 30)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)


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

        #Worktime
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(203, self.height() - 577, 450, 270, Qt.AlignLeft, "Work Time")

        #Descrption worktime
        font_title = QFont()
        font_title.setPointSize(8)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(122, 280, 450, 270, Qt.AlignLeft, "This section presents the")
        painter.drawText(122, 297, 450, 270, Qt.AlignLeft, "duration of engagement")
        painter.drawText(122, 314, 450, 270, Qt.AlignLeft, "in your work.")

        # Breaktime
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(413, self.height() - 577, 450, 270, Qt.AlignLeft, "Break Time")

        font_title = QFont()
        font_title.setPointSize(7)
        painter.setFont(font_title)
        painter.setPen(QColor("#282828"))
        painter.drawText(420, 205, 400, 270, Qt.AlignLeft, "mins")

        # Descrption breaktime
        font_title = QFont()
        font_title.setPointSize(8)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(333, 280, 450, 270, Qt.AlignLeft, "This section shows the")
        painter.drawText(333, 297, 450, 270, Qt.AlignLeft, "period of breaks the ")
        painter.drawText(333, 314, 450, 270, Qt.AlignLeft, "individuals should take.")

        # Breakinterval
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(613, self.height() - 577, 450, 270, Qt.AlignLeft, "Break Interval")

        font_title = QFont()
        font_title.setPointSize(7)
        painter.setFont(font_title)
        painter.setPen(QColor("#282828"))
        painter.drawText(630, 205, 400, 270, Qt.AlignLeft, "mins")

        # Descrption breakinterval
        font_title = QFont()
        font_title.setPointSize(8)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(545, 280, 450, 270, Qt.AlignLeft, "This section shows how")
        painter.drawText(545, 297, 450, 270, Qt.AlignLeft, "often breaks should be")
        painter.drawText(545, 314, 450, 270, Qt.AlignLeft, "taken.")

        # Wrist Position
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(193, 388, 450, 270, Qt.AlignLeft, "Wrist Position")

        # Correct (Wrist Position)
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(180, 470, 450, 270, Qt.AlignLeft, "Correct")

        # Descrption wrist position
        font_title = QFont()
        font_title.setPointSize(8)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(122, 540, 450, 270, Qt.AlignLeft, "This section displays the")
        painter.drawText(122, 557, 450, 270, Qt.AlignLeft, "status of your wrist position")

        # Reminder
        font_title = QFont()
        font_title.setPointSize(11)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(330, 380, 450, 270, Qt.AlignLeft, "Reminders")

        reminder_icon = QPixmap("./src/notif-icon.png")
        painter.drawPixmap(665, self.height() - 345, 45, 40, reminder_icon)

        # Notification message
        notification_top = 430
        notification_height = 30
        spacing = 10

        # Show notification
        if self.notification_container and self.notifications:
            for index, message in enumerate(self.notifications):
                notification_container = QRect(335, notification_top + (index * (notification_height + spacing)), 380,
                                               notification_height)
                painter.setBrush(QColor("#F5F5F5"))
                painter.setPen(Qt.NoPen)
                painter.drawRoundedRect(notification_container, 5, 5)

                font_notification = QFont()
                font_notification.setPointSize(10)
                painter.setFont(font_notification)
                painter.setPen(QColor("#303030"))
                painter.drawText(notification_container, Qt.AlignLeft | Qt.TextWordWrap, message)

        # Camera
        self.camera.cam_container(painter)
        if self.camera.cam_placeholder:
            self.camera.cam_holder(painter)
        else:
            self.camera.cam_draw(painter)

        # Audio
        self.audio.audio_container(painter)
        self.audio.audio_holder(painter)



        #------------IMAGES----------
        # image LOGO
        image_logo = QPixmap("./src/logo.png")
        image_logo_x = self.width() - 450 + (450 - image_logo.width()) // 2
        painter.drawPixmap(image_logo_x, -70, image_logo.width(), image_logo.height(), image_logo)

        # Image GREEN clock
        image_green = QPixmap("./src/green_clock.png")
        painter.drawPixmap(80, self.height() - 605, 130, 75, image_green)

        # Image BLUE clock
        image_blue = QPixmap("./src/blue_clock.png")
        painter.drawPixmap(290, self.height() - 605, 130, 75, image_blue)

        # Image YELLOW clock
        image_yellow = QPixmap("./src/yellow_clock.png")
        painter.drawPixmap(500, self.height() - 605, 130, 75, image_yellow)

        # Image Wrist
        image_yellow = QPixmap("./src/wrist.png")
        painter.drawPixmap(45, 340, 200, 115, image_yellow)

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

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Don't Wrist It",
            timeout=10
        )

        self.notifications.append(message)
        self.notification_container = True
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())