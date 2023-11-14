import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
import cv2
import numpy as np


class ColorTransferWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.source_path = ""
        self.target_path = ""

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.source_label = QLabel("Source Image")
        self.target_label = QLabel("Target Image")
        self.transferred_label = QLabel("Transferred Image")

        layout.addWidget(self.source_label)
        layout.addWidget(self.target_label)
        layout.addWidget(self.transferred_label)

        self.load_source_button = QPushButton("Load Target Image", self)
        self.load_source_button.clicked.connect(self.load_source_image)
        layout.addWidget(self.load_source_button)

        self.load_target_button = QPushButton("Load Source Image", self)
        self.load_target_button.clicked.connect(self.load_target_image)
        layout.addWidget(self.load_target_button)

        self.transfer_button = QPushButton("Transfer Color", self)
        self.transfer_button.clicked.connect(self.perform_color_transfer)
        layout.addWidget(self.transfer_button)

        self.setLayout(layout)

    def load_source_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            self.source_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(self.source_path)
            self.source_label.setPixmap(pixmap)
            self.source_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def load_target_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            self.target_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(self.target_path)
            self.target_label.setPixmap(pixmap)
            self.target_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def perform_color_transfer(self):
        if not (self.source_path and self.target_path):
            return

        # Charger les images source et cible
        source_image = cv2.imread(self.source_path)
        target_image = cv2.imread(self.target_path)

        # Séparer les canaux des images
        source_channels = cv2.split(source_image)
        target_channels = cv2.split(target_image)

        # Calculer les moyennes des canaux pour les images source et cible
        source_channel_means = [np.mean(channel) for channel in source_channels]
        target_channel_means = [np.mean(channel) for channel in target_channels]

        # Calculer les écarts types des canaux pour les images source et cible
        source_channel_stddevs = [np.std(channel) for channel in source_channels]
        target_channel_stddevs = [np.std(channel) for channel in target_channels]

        # Appliquer le transfert de couleur
        transferred_channels = [
            (
                (channel - source_channel_means[i])
                * (target_channel_stddevs[i] / source_channel_stddevs[i])
                + target_channel_means[i]
            ).astype(np.uint8)
            for i, channel in enumerate(source_channels)
        ]

        # Fusionner les canaux transférés
        transferred_image = cv2.merge(transferred_channels)

        # Afficher l'image transférée
        q_image = self.convert_cvimage_to_qimage(transferred_image)
        transferred_pixmap = QPixmap.fromImage(q_image)
        self.transferred_label.setPixmap(transferred_pixmap)
        self.transferred_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        self.central_widget = ColorTransferWidget()
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("Color Transfer Widget")
        self.setGeometry(100, 100, 800, 600)
