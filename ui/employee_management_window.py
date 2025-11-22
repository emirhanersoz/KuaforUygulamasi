from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout,
    QComboBox, QMessageBox
)
from database.db_connection import SessionLocal
from services.employee_service import add_new_employee, get_all_employees
from services.salon_service import get_all_salons

class EmployeeManagementWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Personel Yönetimi")
        
        main_layout = QVBoxLayout()
        
        add_employee_group = QGroupBox("Yeni Personel Kaydı")
        form_layout = QFormLayout()
        
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.salon_combo = QComboBox()
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Çalışan", "Yönetici"]) 
        
        form_layout.addRow("Adı:", self.first_name_input)
        form_layout.addRow("Soyadı:", self.last_name_input)
        form_layout.addRow("E-posta:", self.email_input)
        form_layout.addRow("Şifre:", self.password_input)
        form_layout.addRow("Atanacak Salon:", self.salon_combo)
        form_layout.addRow("Rolü:", self.role_combo)
        
        self.add_button = QPushButton("Personel Ekle")
        self.add_button.clicked.connect(self.handle_add_employee)
        form_layout.addWidget(self.add_button)
        
        add_employee_group.setLayout(form_layout)
        main_layout.addWidget(add_employee_group)

        main_layout.addWidget(QLabel("Mevcut Personeller:"))
        
        self.refresh_btn = QPushButton("Listeyi Getir / Yenile")
        self.refresh_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.refresh_btn.clicked.connect(self.load_all_data)
        main_layout.addWidget(self.refresh_btn)

        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(5)
        self.employee_table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "E-posta", "Salon", "Rol"])
        self.employee_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        main_layout.addWidget(self.employee_table)
        self.setLayout(main_layout)
        
    def load_all_data(self):
        """Hem combobox'ı hem tabloyu doldurur."""
        self.load_salons_to_combo()
        self.load_employee_data()

    def load_salons_to_combo(self):
        self.salon_combo.clear()
        try:
            with SessionLocal() as db:
                salons = get_all_salons(db)
                for s in salons:
                    self.salon_combo.addItem(s.name, s.id)
        except Exception as e:
            print(f"Salonlar combo'ya yüklenemedi: {e}")

    def load_employee_data(self):
        self.employee_table.setRowCount(0)
        try:
            with SessionLocal() as db:
                employees = get_all_employees(db)
                self.employee_table.setRowCount(len(employees))
                for row, emp in enumerate(employees):
                    full_name = f"{emp.user.first_name} {emp.user.last_name}" if emp.user else "Bilinmiyor"
                    email = emp.user.email if emp.user else "-"
                    salon_name = emp.salon.name if emp.salon else "-"
                    role = "Yönetici" if emp.is_admin else "Çalışan"

                    self.employee_table.setItem(row, 0, QTableWidgetItem(str(emp.id)))
                    self.employee_table.setItem(row, 1, QTableWidgetItem(full_name))
                    self.employee_table.setItem(row, 2, QTableWidgetItem(email))
                    self.employee_table.setItem(row, 3, QTableWidgetItem(salon_name))
                    self.employee_table.setItem(row, 4, QTableWidgetItem(role))
            QMessageBox.information(self, "Bilgi", "Veriler başarıyla yüklendi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Personel verisi çekilemedi: {e}")

    def handle_add_employee(self):
        f_name = self.first_name_input.text()
        l_name = self.last_name_input.text()
        email = self.email_input.text()
        pwd = self.password_input.text()
        
        salon_id = self.salon_combo.currentData()
        role = self.role_combo.currentText()

        if not f_name or not email or not pwd:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return
        
        if not salon_id:
             QMessageBox.warning(self, "Uyarı", "Lütfen önce 'Yenile' butonuna basıp salonları yükleyin ve bir salon seçin.")
             return

        try:
            with SessionLocal() as db:
                new_emp = add_new_employee(db, f_name, l_name, email, pwd, salon_id, role)
                if new_emp:
                    QMessageBox.information(self, "Başarılı", "Personel eklendi.")
                    self.load_employee_data()
                    self.first_name_input.clear()
                    self.last_name_input.clear()
                    self.email_input.clear()
                    self.password_input.clear()
                else:
                    QMessageBox.critical(self, "Hata", "Personel eklenemedi (E-posta kullanımda olabilir).")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir sorun oluştu: {e}")