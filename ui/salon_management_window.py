import sys

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTabWidget, QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout, QApplication, QMessageBox
)
from PyQt6.QtCore import Qt

class SalonManagementWindow(QWidget):
    """
    Yöneticilerin salonları, hizmetleri ve çalışma saatlerini yönettiği ana ekran.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Salon Yönetimi")
        
        main_layout = QVBoxLayout()

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.salon_tab = QWidget()
        self.tabs.addTab(self.salon_tab, "Salonlar")
        self.setup_salon_tab()

        self.services_tab = QWidget()
        self.tabs.addTab(self.services_tab, "Hizmetler ve Ücretler")
        self.setup_services_tab()

        self.setLayout(main_layout)

    def setup_salon_tab(self):
        """Salonlar sekmesinin arayüzünü oluşturur."""
        layout = QVBoxLayout(self.salon_tab)

        add_salon_group = QGroupBox("Yeni Salon Tanımla")
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.address_input = QLineEdit()
        self.phone_input = QLineEdit()
        
        form_layout.addRow("Salon Adı:", self.name_input)
        form_layout.addRow("Adres:", self.address_input)
        form_layout.addRow("Telefon:", self.phone_input)
        
        self.add_button = QPushButton("Salon Ekle")
        form_layout.addWidget(self.add_button)
        
        add_salon_group.setLayout(form_layout)
        layout.addWidget(add_salon_group)
        

        layout.addWidget(QLabel("Mevcut Salonlar:"))
        self.salon_table = QTableWidget()
        self.salon_table.setColumnCount(4)
        self.salon_table.setHorizontalHeaderLabels(["ID", "Ad", "Telefon", "Durum"])
        self.salon_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.load_salon_data()
        
        layout.addWidget(self.salon_table)

    def setup_services_tab(self):
        """Hizmetler sekmesinin arayüzünü oluşturur."""
        layout = QVBoxLayout(self.services_tab)
        
        layout.addWidget(QLabel("Hizmetler Yönetimi (Yakında)"), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QPushButton("Yeni Hizmet Ekle"), alignment=Qt.AlignmentFlag.AlignCenter)

    def load_salon_data(self):
        """Örnek salon verilerini tabloya yükler."""
        sample_data = [
            (1, "Merkez Şube", "555-1234", "Aktif"),
            (2, "Anadolu Yakası", "555-5678", "Aktif"),
            (3, "Test Salonu", "555-0000", "Pasif"),
        ]
        
        self.salon_table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, item in enumerate(data):
                self.salon_table.setItem(row, col, QTableWidgetItem(str(item)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SalonManagementWindow()
    window.show()
    sys.exit(app.exec())