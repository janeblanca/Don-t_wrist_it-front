from PyQt5.QtGui import QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt, QRect


class Worktime:
    def __init__(self, parent):
        self.parent = parent
        self.worktime_placeholder = True
        self.total_work_time = 0

    def worktime_container(self, painter):
        # WORKTIME
        color = QColor("#FFFFFF")
        worktime = QRect(105, 115, 200, 230)
        painter.setBrush(color)
        painter.setPen(color)
        painter.setBrush(QColor("#FFFFFF"))
        radius = 8
        painter.drawRoundedRect(worktime, radius, radius)

    def worktime_holder(self, painter):
        # small square ICON (Green Clock)
        color = QColor("#D0FFCF")
        square_green_box = QRect(119, self.parent.height() - 593, 50, 50)
        painter.setBrush(color)
        painter.setPen(color)
        painter.setBrush(QColor("#D0FFCF"))
        radius = 8
        painter.drawRoundedRect(square_green_box, radius, radius)

        # small square (Worktime)
        painter.setBrush(QColor("#D0FFCF"))
        square_green_box = QRect(185, self.parent.height() - 583, 105, 30)
        radius = 8
        painter.drawRoundedRect(square_green_box, radius, radius)

        # Worktime
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(203, self.parent.height() - 577, 450, 270, Qt.AlignLeft, "Work Time")

        # Description worktime
        font_title = QFont()
        font_title.setPointSize(8)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(122, 280, 450, 270, Qt.AlignLeft, "This section presents the")
        painter.drawText(122, 297, 450, 270, Qt.AlignLeft, "duration of engagement")
        painter.drawText(122, 314, 450, 270, Qt.AlignLeft, "in your work.")

        # Display Total Work Time
        font_counter = QFont()
        font_counter.setPointSize(10)
        painter.setFont(font_counter)
        painter.setPen(QColor("#303030"))
        painter.drawText(140, 200, 150, 30, Qt.AlignLeft, "Time Work Time:")
        painter.drawText(180, 240, 150, 30, Qt.AlignLeft, f"{self.parent.format_time(self.parent.total_work_time)}")

        # Image GREEN clock
        image_green = QPixmap("./src/green_clock.png")
        painter.drawPixmap(80, self.parent.height() - 605, 130, 75, image_green)

    def update(self):
        self.parent.update()