import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTabWidget, QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout,
    QMessageBox
)
from PyQt6.QtCore import Qt

from database.db_connection import SessionLocal 
from services.salon_service import create_salon, get_all_salons

class SalonManagementWindow(QWidget):
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
        self.add_button.clicked.connect(self.add_new_salon)
        form_layout.addWidget(self.add_button)
        
        add_salon_group.setLayout(form_layout)
        layout.addWidget(add_salon_group)
        
        layout.addWidget(QLabel("Mevcut Salonlar:"))
        self.salon_table = QTableWidget()
        self.salon_table.setColumnCount(4)
        self.salon_table.setHorizontalHeaderLabels(["ID", "Ad", "Telefon", "Durum"])
        self.salon_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.salon_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.salon_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
     
        layout.addWidget(self.salon_table)

        self.refresh_btn = QPushButton("Verileri Yükle / Yenile")
        self.refresh_btn.clicked.connect(self.load_salon_data)
        layout.addWidget(self.refresh_btn)

    def setup_services_tab(self):
        layout = QVBoxLayout(self.services_tab)
        layout.addWidget(QLabel("Hizmetler Yönetimi (Yakında)"), alignment=Qt.AlignmentFlag.AlignCenter)

    def load_salon_data(self):
        self.salon_table.setRowCount(0)

        print("Salon verileri çekiliyor...")
        try:
            with SessionLocal() as db:
                salons = get_all_salons(db)
                self.salon_table.setRowCount(len(salons))
                for row, salon in enumerate(salons):
                    status = "Aktif" if salon.is_active else "Pasif"
                    self.salon_table.setItem(row, 0, QTableWidgetItem(str(salon.id)))
                    self.salon_table.setItem(row, 1, QTableWidgetItem(salon.name))
                    self.salon_table.setItem(row, 2, QTableWidgetItem(salon.phone_number or ""))
                    self.salon_table.setItem(row, 3, QTableWidgetItem(status))
            print("Salon verileri başarıyla yüklendi.")
        except Exception as e:
            print(f"HATA OLUŞTU: {e}")
            QMessageBox.critical(self, "Hata", f"Veriler yüklenirken hata oluştu: {e}")

    def add_new_salon(self):
        name = self.name_input.text().strip()
        address = self.address_input.text().strip()
        phone = self.phone_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Uyarı", "Salon adı boş bırakılamaz.")
            return

        try:
            with SessionLocal() as db:
                create_salon(db, name, address, phone)
                QMessageBox.information(self, "Başarılı", "Yeni salon başarıyla eklendi.")
                
                self.name_input.clear()
                self.address_input.clear()
                self.phone_input.clear()
                
                self.load_salon_data()
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Salon eklenirken bir hata oluştu: {e}")