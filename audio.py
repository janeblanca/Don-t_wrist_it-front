# audio.py

from PyQt5.QtGui import QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt, QRect
from gtts import gTTS
import os


class Audio:
    def __init__(self, parent):
        self.parent = parent
        self.audio_placeholder = True

    def audio_container(self, painter):
        color = QColor("#E8E7E7")
        painter.setBrush(color)
        painter.setBrush(color)
        painter.setPen(color)
        painter.setBrush(QColor("#E8E7E7"))
        audio_pane = QRect(105, self.parent.height() - 115, self.parent.width() - 577, 85)
        radius = 13
        painter.drawRoundedRect(audio_pane, radius, radius)

    def speak_text(self):
        text_to_speak = "Prolonged incorrect wrist position! Correct your position immediately."
        tts = gTTS(text=text_to_speak, lang='en')
        tts.save("audio.mp3")
        os.system("start audio.mp3")

    def audio_holder(self, painter):
        # small square (box of audio icon)
        image_audio = QPixmap("./src/audio_icon.png")
        color = QColor("#FBF0F3")
        painter.setBrush(color)
        painter.setPen(color)
        painter.setBrush(QColor("#FBF0F3"))
        square_audio_box = QRect(123, self.parent.height() - 100, 50, 50)
        radius = 8
        painter.drawRoundedRect(square_audio_box, radius, radius)

        # Audio Icon
        audio_icon_rect = QRect(126, self.parent.height() - 100, 45, 45)
        painter.drawPixmap(audio_icon_rect, image_audio)

        # Audio Line
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(200, self.parent.height() - 85, 450, 270, Qt.AlignLeft,
                         "Prolonged incorrect wrist position! Correct your position immediately.")

    def update(self):
        self.parent.update()
