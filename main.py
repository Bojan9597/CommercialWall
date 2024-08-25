from PySide6.QtWidgets import QApplication, QMainWindow
from CommercialClass import CommercialClass

if __name__ == "__main__":
    app = QApplication([])

    # Create a QMainWindow to hold the CommercialClass widget
    main_window = QMainWindow()

    # Create an instance of CommercialClass (no arguments)
    commercial_manager = CommercialClass()

    # Set the central widget of the main window to the video widget from CommercialClass
    main_window.setCentralWidget(commercial_manager.video_widget)

    # Show the main window in full screen mode
    main_window.showFullScreen()

    # Start the application
    app.exec()
