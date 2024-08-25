from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Signal, QUrl, Qt
from PySide6.QtGui import QPixmap, QFont, QPainter
import os
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

class VideoWidget(QWidget):
    # Signal emitted when the video finishes playing
    video_finished = Signal()

    def __init__(self):
        super().__init__()
        
        # Setup layout and video player
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Create a video widget and media player
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        # Make the video widget stretch to fill the available space
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create a placeholder for the image
        self.placeholder_image = None
        self.load_placeholder_image('images/breathalyzerImage.jpg')
        
        # Media player setup
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)
        
        # Connect the media player's stateChanged signal to detect when the video finishes
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)
        
        # Initially show the placeholder image and hide the video widget
        self.show_placeholder()
        self.show_text = True

    def load_placeholder_image(self, image_path):
        # Load the placeholder image from the specified path
        if os.path.exists(image_path):
            self.placeholder_image = QPixmap(image_path)
        else:
            print(f"Image file {image_path} does not exist.")

    def show_placeholder(self):
        # Show the placeholder image by enabling the paintEvent and hiding the video widget
        self.show_text = True
        self.video_widget.hide()
        self.update()

    def hide_placeholder(self):
        # Hide the placeholder image by disabling the paintEvent and showing the video widget
        self.show_text = False
        self.video_widget.show()
        self.update()

    def play_video(self, video_path):
        if os.path.exists(video_path):
            # Set the video source and start playing
            video_url = QUrl.fromLocalFile(video_path)
            self.media_player.setSource(video_url)
            self.media_player.play()
            
            # Hide the placeholder image and text, and show the video widget
            self.hide_placeholder()
        else:
            print(f"Video file {video_path} does not exist.")
    
    def on_media_status_changed(self, status):
        # Check if the media has finished playing
        if status == QMediaPlayer.EndOfMedia:
            # Emit the video finished signal and show the placeholder image and text
            self.video_finished.emit()

    def paintEvent(self, event):
        # If show_text is True, paint the placeholder image and text
        if self.placeholder_image and self.show_text:
            painter = QPainter(self)

            # Draw the placeholder image
            painter.drawPixmap(self.rect(), self.placeholder_image)

            # Set up the font and color for the text
            painter.setFont(QFont("Arial", 30, QFont.Bold))
            painter.setPen(Qt.white)

            # Draw the text in the center of the widget
            text = "Fetching next video..."
            text_rect = painter.fontMetrics().boundingRect(self.rect(), Qt.AlignCenter, text)
            painter.drawText(self.rect(), Qt.AlignCenter, text)

            painter.end()
