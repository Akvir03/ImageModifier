import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QImage, QPixmap, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
    QColorDialog,
)
import cv2
import numpy as np


class ChromaticAdaptationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.image_path = ""
        self.target_color = QColor(0, 128, 0)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.original_label = QLabel("Original Image")
        self.adapted_label = QLabel("Adapted Image")

        layout.addWidget(self.original_label)
        layout.addWidget(self.adapted_label)

        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        self.choose_color_button = QPushButton("Choose Color", self)
        self.choose_color_button.clicked.connect(self.choose_target_color)
        layout.addWidget(self.choose_color_button)

        self.adapt_button = QPushButton("Adapt Image", self)
        self.adapt_button.clicked.connect(self.chromatic_adaptation)
        layout.addWidget(self.adapt_button)

        self.setLayout(layout)

    def load_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            self.image_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(self.image_path)
            self.original_label.setPixmap(pixmap)
            self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def choose_target_color(self):
        color_dialog = QColorDialog(self)
        color_dialog.setCurrentColor(self.target_color)

        if color_dialog.exec() == QColorDialog.DialogCode.Accepted:
            self.target_color = color_dialog.currentColor()

    def chromatic_adaptation(self):
        if not self.image_path:
            return

        # Charger l'image
        image = cv2.imread(self.image_path)

        # Séparer les canaux de l'image
        channels = cv2.split(image)

        # Calculer les moyennes des canaux
        channel_means = [np.mean(channel) for channel in channels]

        # Adapter chromatiquement chaque canal
        adapted_channels = [
            np.minimum(
                np.maximum(
                    (channel - np.min(channel_means))
                    / (np.max(channel_means) - np.min(channel_means))
                    * (self.target_color.green() - 0)
                    + 0,
                    0,
                ),
                255,
            ).astype(np.uint8)
            for channel in channels
        ]

        # Fusionner les canaux adaptés
        adapted_image = cv2.merge(adapted_channels)

        # Afficher l'image adaptée
        q_image = self.convert_cvimage_to_qimage(adapted_image)
        adapted_pixmap = QPixmap.fromImage(q_image)
        self.adapted_label.setPixmap(adapted_pixmap)
        self.adapted_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def convert_cvimage_to_qimage(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width

        # Convertir l'image OpenCV en format RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Créer un objet QImage à partir des données de l'image
        q_image = QImage(
            rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
        )

        return q_image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = ChromaticAdaptationWidget()
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("Chromatic Adaptation Widget")
        self.setGeometry(100, 100, 800, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
