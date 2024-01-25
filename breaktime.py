from PyQt5.QtGui import QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt, QRect


class Breaktime:
    def __init__(self, parent):
        self.parent = parent
        self.breaktime_placeholder = True
        self.total_work_time = 0



    def breaktime_container(self, painter):
        # BREAKTIME
        color = QColor("#FFFFFF")
        painter.setBrush(color)
        painter.setPen(color)
        painter.setBrush(QColor("#FFFFFF"))
        breaktime = QRect(317, 115, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(breaktime, radius, radius)

    def breaktime_holder(self, painter):
        # small square ICON (BLue Clock)
        color = QColor("#D0FBFF")
        painter.setBrush(color)
        painter.setPen(color)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(329, self.parent.height() - 593, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)

        # small square (Breaktime)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(395, self.parent.height() - 583, 105, 30)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)

        # Breaktime
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(413, self.parent.height() - 577, 450, 270, Qt.AlignLeft, "Break Time")

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

        # Image BLUE clock
        image_blue = QPixmap("./src/blue_clock.png")
        painter.drawPixmap(290, self.parent.height() - 605, 130, 75, image_blue)


    def update(self):
        self.parent.update()