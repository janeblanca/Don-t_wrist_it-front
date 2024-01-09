import sys
from PyQt5.QtWidgets import QApplication, QWidget,  QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QIntValidator
from PyQt5.QtCore import Qt, QRect
import cv2

from camera import Camera

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the UI components
        self.init_ui()

        # Disable maximized window
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.show_camera = False
        self.camera = Camera(self)
        self.timer = self.startTimer(1)

        #
        self.user_input = QLineEdit(self)
        self.user_input.setGeometry(355, 195, 50, 40)
        self.user_input.setStyleSheet( "background-color: #f3f1ec; border: none; color: #303030; font-size: 30px;")

        # accept integers only
        int_validator = QIntValidator()
        self.user_input.setValidator(int_validator)


        self.user_input.returnPressed.connect(self.set_break_time)
        self.break_time = 0

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

        # AUDIO
        painter.setBrush(QColor(74, 73, 73, int(0.23 * 255)))
        audio_pane = QRect(105, self.height() - 115, self.width() - 577, 85)
        radius = 13  # Set the radius for rounded corners
        painter.drawRoundedRect(audio_pane, radius, radius)

        # small square (box of audio icon)
        painter.setBrush(QColor("#FBF0F3"))
        square_audio_box = QRect(123, self.height() - 97, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_audio_box, radius, radius)

        # WORKTIME
        painter.setBrush(QColor("#FFFFFF"))
        # worktime = QRect(105, self.height() - 600, self.width() - 1000, self.height() - 520)
        worktime= QRect(105, 115, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(worktime, radius, radius)

        # small square ICON (Green Clock)
        painter.setBrush(QColor("#D0FFCF"))
        square_green_box= QRect(119, self.height() - 593, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_green_box, radius, radius)

        # small square ICON (Worktime)
        painter.setBrush(QColor("#D0FFCF"))
        square_green_box = QRect(118, self.height() - 475,105, 30)
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

        # small square ICON (Breaktime)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(328, self.height() - 475, 105, 30)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)

        # BREAk INTERVAL
        painter.setBrush(QColor("#FFFFFF"))
        breakinterval = QRect(529, 115, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(breakinterval, radius, radius)

        # small square ICON (Yellow Clock)
        painter.setBrush(QColor("#FFF7AE"))
        square_yellow_box = QRect(540, self.height() - 593, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_yellow_box, radius, radius)

        # small square ICON (Break Interval)
        painter.setBrush(QColor("#FFF7AE"))
        square_yellow_box = QRect(539, self.height() - 475, 105, 30)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_yellow_box, radius, radius)

        # WRIST POSITION
        painter.setBrush(QColor("#FFFFFF"))
        worktime = QRect(105, 360, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(worktime, radius, radius)

        # Reminder
        painter.setBrush(QColor("#FFFFFF"))
        reminder = QRect(317, 360, self.width() - 788, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(reminder, radius, radius)

        # small square ICON (Wrist Position)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(119, self.height() - 347, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)

        # small square ICON (Correct - Wrist Position)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(118, 496, 105, 30)
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

        # Audio Line
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(200, self.height()-85, 450, 270, Qt.AlignLeft, "Prolonged incorrect wrist position! Correct your position immediately.")

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
        painter.drawText(134, 250, 450, 270, Qt.AlignLeft, "Work Time")

        # Breaktime
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(344, 250, 450, 270, Qt.AlignLeft, "Break Time")

        font_title = QFont()
        font_title.setPointSize(7)
        painter.setFont(font_title)
        painter.setPen(QColor("#282828"))
        painter.drawText(420, 205, 400, 270, Qt.AlignLeft, "mins")

        # Breakinterval
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(545, 250, 450, 270, Qt.AlignLeft, "Break Interval")

        font_title = QFont()
        font_title.setPointSize(7)
        painter.setFont(font_title)
        painter.setPen(QColor("#282828"))
        painter.drawText(630, 205, 400, 270, Qt.AlignLeft, "mins")

        # Wrist Position
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(190, 390, 450, 270, Qt.AlignLeft, "Wrist Position")

        # Correct (Wrist Position)
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(149, 501, 450, 270, Qt.AlignLeft, "Correct")

        # Reminder
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(335, 390, 450, 270, Qt.AlignLeft, "Reminder")

        # Camera
        self.camera.cam_container(painter)
        if self.camera.cam_placeholder:
            self.camera.cam_holder(painter)
        else:
            self.camera.cam_draw(painter)


        #------------IMAGES----------
        # image LOGO
        image_logo = QPixmap("./src/logo.png")
        image_logo_x = self.width() - 450 + (450 - image_logo.width()) // 2
        painter.drawPixmap(image_logo_x, -70, image_logo.width(), image_logo.height(), image_logo)

        # Image AUDIO
        image_audio = QPixmap("./src/audio_icon.png")
        painter.drawPixmap(133, self.height()- 88, 32,30,image_audio)

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
            camera_rect = QRect(self.width() - 420, 330, 390, 350)
            if camera_rect.contains(click_pos):
                print("Clicked!")
                self.camera.cam_placeholder = not self.camera.cam_placeholder
                self.update()
        super().mousePressEvent(event)

    def timerEvent(self, event):
        if event.timerId() == self.timer:
            self.camera.update()

    def closeEvent(self, event):
        self.camera.release_camera()
        event.accept()

    def set_break_time(self):
        # Get the break time duration
        break_time_str = self.user_input.text()
        try:
            self.break_time = int(break_time_str)
            print(f"Break time set to {self.break_time} minutes.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for break time.")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
