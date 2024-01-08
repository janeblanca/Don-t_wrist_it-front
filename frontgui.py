import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt, QRect


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

    def init_ui(self):
        self.setWindowTitle("Don't Wrist It")
        self.setGeometry(350, 200, 1280, 720)
        self.setStyleSheet("background-color: #f3f1ec;")
        self.setFixedSize(1280, 720) # fixed size

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
        audio_pane = QRect(105, self.height() - 125, self.width() - 577, 85)
        radius = 13  # Set the radius for rounded corners
        painter.drawRoundedRect(audio_pane, radius, radius)

        # small square (box of audio icon)
        painter.setBrush(QColor("#CF6B6E"))
        square_audio_box = QRect(123, self.height() - 110, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_audio_box, radius, radius)

        # WORKTIME
        painter.setBrush(QColor("#FFFFFF"))
        worktime= QRect(105, self.height() - 600, 200, 200)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(worktime, radius, radius)

        # BREAKTIME
        painter.setBrush(QColor("#FFFFFF"))
        breaktime = QRect(357, self.height() - 600, 200, 200)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(breaktime, radius, radius)

        # BREAk INTERVAL
        painter.setBrush(QColor("#FFFFFF"))
        breakinterval = QRect(608 , self.height() - 600, 200, 200)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(breakinterval, radius, radius)

        # WRIST POSITION
        painter.setBrush(QColor("#FFFFFF"))
        worktime = QRect(105, self.height() - 360, 200, 200)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(worktime, radius, radius)

        # Reminder
        painter.setBrush(QColor("#FFFFFF"))
        reminder = QRect(357, self.height() - 360, self.width() - 828, 200)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(reminder, radius, radius)

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
        painter.drawText(200, self.height()-95, 450, 270, Qt.AlignLeft, "Prolonged incorrect wrist position! Correct your position immediately.")

        # Don't Wrist It (Logo)
        font_title2 = QFont()
        font_title2.setPointSize(13)
        painter.setFont(font_title2)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(self.width() - 450, 100, 450, 270, Qt.AlignCenter, "DON'T WRIST IT")

        painter.setPen(QColor("#4F4E4E"))
        painter.drawLine(self.width() - 420, 275, self.width() - 43, 275)

        # Setting-up Camera
        font_desc = QFont()
        font_desc.setPointSize(10)
        painter.setFont(font_desc)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(self.width() - 420, 295, 450, self.height(), Qt.AlignLeft, "Setting-up your Camera")

       # Camera
        self.camera.cam_container(painter)
        if self.camera.cam_placeholder:
            self.camera.cam_holder(painter)
        else:
            self.camera.cam_draw(painter)

        #Worktime
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(150, 260, 450, 270, Qt.AlignLeft, "Work Time")

        #------------IMAGES----------
        # image LOGO
        image_logo = QPixmap("./src/logo.png")
        image_logo_x = self.width() - 450 + (450 - image_logo.width()) // 2
        painter.drawPixmap(image_logo_x, -70, image_logo.width(), image_logo.height(), image_logo)

        # Image AUDIO
        image_audio = QPixmap("./src/audio_icon.png")
        painter.drawPixmap(136, self.height()-98, 27, 27,image_audio)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
