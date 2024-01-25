from PyQt5.QtGui import QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt, QRect
from plyer import notification  # Import the notification module

class Reminder:
    def __init__(self, parent):
        self.parent = parent

        # Store Notification message
        self.parent.notification_message = ""
        self.parent.notification_container = False
        self.parent.notifications = []

    def reminder_container(self, painter):
        # Reminder
        pen = QPen(QColor("#FFFFFF"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#FFFFFF"))
        reminder = QRect(317, 360, self.parent.width() - 788, 230)
        radius = 8  # Set the radius for rounded corners
        painter.drawRoundedRect(reminder, radius, radius)


    def reminder_holder(self, painter):
        # Reminder
        font_title = QFont()
        font_title.setPointSize(11)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(330, 380, 450, 270, Qt.AlignLeft, "Reminders")

        reminder_icon = QPixmap("./src/notif-icon.png")
        painter.drawPixmap(665, self.parent.height() - 345, 45, 40, reminder_icon)

        # Notification message
        notification_top = 430
        notification_height = 30
        spacing = 10

        # Show notification
        if self.parent.notification_container and self.parent.notifications:
            for index, message in enumerate(self.parent.notifications):
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

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Don't Wrist It",
            timeout=10
        )

        self.parent.notifications.append(message)
        self.parent.notification_container = True
        self.parent.update()

    def update(self):
        self.parent.update()
