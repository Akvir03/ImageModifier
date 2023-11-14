import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from adaptRGB import ChromaticAdaptationWidget
from transferRGB import ColorTransferWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QStackedWidget()
        self.setup_widgets()

        self.sidebar = QListWidget()
        self.setup_sidebar()

        layout = QVBoxLayout()
        layout.addWidget(self.sidebar, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.central_widget)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setWindowTitle("PictureModifier")
        self.setGeometry(100, 100, 800, 600)

    def setup_widgets(self):
        self.chromatic_adaptation_widget = ChromaticAdaptationWidget()
        self.color_transfer_widget = ColorTransferWidget()

        self.central_widget.addWidget(self.chromatic_adaptation_widget)
        self.central_widget.addWidget(self.color_transfer_widget)

    def setup_sidebar(self):
        items = [
            {"text": "Chromatic Adaptation"},
            {"text": "Color Transfer"},
        ]

        for item_data in items:
            item = QListWidgetItem(item_data["text"])
            self.sidebar.addItem(item)

        self.sidebar.currentRowChanged.connect(self.change_widget)

    def change_widget(self, index):
        self.central_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
