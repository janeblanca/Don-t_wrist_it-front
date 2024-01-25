from PyQt5.QtGui import QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt, QRect


class BreakInterval:
    def __init__(self, parent):
        self.parent = parent

    def breakinterval_container(self, painter):
        # BREAk INTERVAL
        pen = QPen(QColor("#FFFFFF"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#FFFFFF"))
        breakinterval = QRect(529, 115, 200, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(breakinterval, radius, radius)

    def breakinterval_holder(self, painter):
        # small square ICON (Yellow Clock)
        painter.setBrush(QColor("#FFF7AE"))
        square_yellow_box = QRect(540, self.parent.height() - 593, 50, 50)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_yellow_box, radius, radius)

        # small square(Break Interval)
        painter.setBrush(QColor("#FFF7AE"))
        square_yellow_box = QRect(607, self.parent.height() - 583, 105, 30)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(square_yellow_box, radius, radius)

        # Breakinterval
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(613, self.parent.height() - 577, 450, 270, Qt.AlignLeft, "Break Interval")

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

        # Image YELLOW clock
        image_yellow = QPixmap("./src/yellow_clock.png")
        painter.drawPixmap(500, self.parent.height() - 605, 130, 75, image_yellow)

    def update(self):
        self.parent.update()