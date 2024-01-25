from PyQt5.QtGui import QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt, QRect


class WristPosition:
    def __init__(self, parent):
        self.parent = parent

    def wristposition_container(self, painter):
        # WRIST POSITION
        pen = QPen(QColor("#FFFFFF"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#FFFFFF"))
        wristposition = QRect(105, 360, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(wristposition, radius, radius)

    def wristposition_holder(self, painter):
        # small square ICON (Wrist Position)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(119, self.parent.height() - 347, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)

        # small square (Correct - Wrist Position)
        painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(183, 382, 105, 30)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_blue_box, radius, radius)

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

        # Image Wrist
        image_yellow = QPixmap("./src/wrist.png")
        painter.drawPixmap(45, 340, 200, 115, image_yellow)

    def update(self):
        self.parent.update()