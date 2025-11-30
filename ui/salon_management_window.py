import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout,
    QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from database.db_connection import SessionLocal
from services.salon_service import create_salon, get_all_salons, update_salon

class SalonManagementWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Salon Yönetimi")
        self.current_salon_id = None
        
        main_layout = QVBoxLayout()

        form_group = QGroupBox("Salon İşlemleri")
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.address_input = QLineEdit()
        self.phone_input = QLineEdit()
        
        form_layout.addRow("Salon Adı:", self.name_input)
        form_layout.addRow("Adres:", self.address_input)
        form_layout.addRow("Telefon:", self.phone_input)
        
        btn_layout = QHBoxLayout()
        self.save_button = QPushButton("Ekle")
        self.save_button.clicked.connect(self.handle_save)
        
        self.clear_button = QPushButton("Temizle / Yeni")
        self.clear_button.clicked.connect(self.clear_form)
        
        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.clear_button)
        form_layout.addRow(btn_layout)
        
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)
        
        self.salon_table = QTableWidget()
        self.salon_table.setColumnCount(4)
        self.salon_table.setHorizontalHeaderLabels(["ID", "Ad", "Telefon", "Adres"])
        self.salon_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.salon_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.salon_table.itemClicked.connect(self.on_row_clicked)
        
        main_layout.addWidget(self.salon_table)
        self.setLayout(main_layout)
        self.load_salon_data()

    def load_salon_data(self):
        self.salon_table.setRowCount(0)
        try:
            with SessionLocal() as db:
                salons = get_all_salons(db)
                self.salon_table.setRowCount(len(salons))
                for row, salon in enumerate(salons):
                    self.salon_table.setItem(row, 0, QTableWidgetItem(str(salon.id)))
                    self.salon_table.setItem(row, 1, QTableWidgetItem(salon.name))
                    self.salon_table.setItem(row, 2, QTableWidgetItem(salon.phone_number or ""))
                    self.salon_table.setItem(row, 3, QTableWidgetItem(salon.address or ""))
        except Exception as e:
            print(f"Hata: {e}")

    def on_row_clicked(self, item):
        row = item.row()
        self.current_salon_id = int(self.salon_table.item(row, 0).text())
        
        self.name_input.setText(self.salon_table.item(row, 1).text())
        self.phone_input.setText(self.salon_table.item(row, 2).text())
        self.address_input.setText(self.salon_table.item(row, 3).text())
        
        self.save_button.setText("Güncelle")

    def clear_form(self):
        self.current_salon_id = None
        self.name_input.clear()
        self.address_input.clear()
        self.phone_input.clear()
        self.save_button.setText("Ekle")
        self.salon_table.clearSelection()

    def handle_save(self):
        name = self.name_input.text().strip()
        address = self.address_input.text().strip()
        phone = self.phone_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Uyarı", "Salon adı boş olamaz.")
            return

        try:
            with SessionLocal() as db:
                if self.current_salon_id:
                    if update_salon(db, self.current_salon_id, name, address, phone):
                        QMessageBox.information(self, "Başarılı", "Salon güncellendi.")
                    else:
                        QMessageBox.warning(self, "Hata", "Güncelleme başarısız.")
                else:
                    create_salon(db, name, address, phone)
                    QMessageBox.information(self, "Başarılı", "Yeni salon eklendi.")
            
            self.clear_form()
            self.load_salon_data()
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İşlem hatası: {e}")