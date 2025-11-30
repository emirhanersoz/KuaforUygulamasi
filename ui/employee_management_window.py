from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout,
    QComboBox, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from database.db_connection import SessionLocal
from services.employee_service import add_new_employee, get_all_employees, update_employee
from services.salon_service import get_all_salons

class EmployeeManagementWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Personel Yönetimi")
        self.current_emp_id = None
        
        main_layout = QVBoxLayout()
        
        form_group = QGroupBox("Personel İşlemleri")
        form_layout = QFormLayout()
        
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Güncellemede boş bırakırsanız değişmez (Opsiyonel)")
        
        self.salon_combo = QComboBox()
        self.role_combo = QComboBox()
        self.role_combo.addItem("Çalışan", 2)
        self.role_combo.addItem("Yönetici", 3)
        
        form_layout.addRow("Ad:", self.first_name_input)
        form_layout.addRow("Soyad:", self.last_name_input)
        form_layout.addRow("E-posta:", self.email_input)
        form_layout.addRow("Şifre:", self.password_input)
        form_layout.addRow("Salon:", self.salon_combo)
        form_layout.addRow("Rol:", self.role_combo)
        
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

        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(6)
        self.employee_table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "E-posta", "Salon", "Rol", "SalonID_Gizli"])
        self.employee_table.setColumnHidden(5, True)
        self.employee_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.employee_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.employee_table.itemClicked.connect(self.on_row_clicked)
        
        main_layout.addWidget(self.employee_table)
        self.setLayout(main_layout)
        
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
            print(f"Salon yükleme hatası: {e}")

    def load_employee_data(self):
        self.employee_table.setRowCount(0)
        try:
            with SessionLocal() as db:
                employees = get_all_employees(db)
                self.employee_table.setRowCount(len(employees))
                for row, emp in enumerate(employees):
                    full_name = f"{emp.user.first_name} {emp.user.last_name}" if emp.user else "?"
                    email = emp.user.email if emp.user else "-"
                    salon_name = emp.salon.name if emp.salon else "-"
                    salon_id = emp.salon_id if emp.salon else 0
                    role = "Yönetici" if emp.is_admin else "Çalışan"

                    self.employee_table.setItem(row, 0, QTableWidgetItem(str(emp.id)))
                    self.employee_table.setItem(row, 1, QTableWidgetItem(full_name))
                    self.employee_table.setItem(row, 2, QTableWidgetItem(email))
                    self.employee_table.setItem(row, 3, QTableWidgetItem(salon_name))
                    self.employee_table.setItem(row, 4, QTableWidgetItem(role))
                    self.employee_table.setItem(row, 5, QTableWidgetItem(str(salon_id)))
        except Exception as e:
            print(f"Personel yükleme hatası: {e}")

    def on_row_clicked(self, item):
        row = item.row()
        self.current_emp_id = int(self.employee_table.item(row, 0).text())
        full_name = self.employee_table.item(row, 1).text()
        email = self.employee_table.item(row, 2).text()
        salon_id = int(self.employee_table.item(row, 5).text())
        role_text = self.employee_table.item(row, 4).text()
        
        parts = full_name.split(" ", 1)
        self.first_name_input.setText(parts[0])
        self.last_name_input.setText(parts[1] if len(parts)>1 else "")
        self.email_input.setText(email)
        
        index = self.salon_combo.findData(salon_id)
        if index >= 0: self.salon_combo.setCurrentIndex(index)
        
        role_target = 3 if role_text == "Yönetici" else 2
        r_index = self.role_combo.findData(role_target)
        if r_index >= 0: self.role_combo.setCurrentIndex(r_index)
        
        self.save_button.setText("Güncelle")

    def clear_form(self):
        self.current_emp_id = None
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.save_button.setText("Ekle")
        self.employee_table.clearSelection()

    def handle_save(self):
        f_name = self.first_name_input.text()
        l_name = self.last_name_input.text()
        email = self.email_input.text()
        pwd = self.password_input.text()
        salon_id = self.salon_combo.currentData()
        role_id = self.role_combo.currentData()

        if not f_name or not email or not salon_id:
             QMessageBox.warning(self, "Uyarı", "Ad, Soyad ve E-posta zorunludur.")
             return

        try:
            with SessionLocal() as db:
                if self.current_emp_id:
                    if update_employee(db, self.current_emp_id, f_name, l_name, email, salon_id, role_id):
                        QMessageBox.information(self, "Başarılı", "Personel güncellendi.")
                    else:
                        QMessageBox.warning(self, "Hata", "Güncelleme başarısız.")
                else:
                    if not pwd:
                        QMessageBox.warning(self, "Uyarı", "Yeni kayıt için şifre zorunludur.")
                        return
                    new_emp = add_new_employee(db, f_name, l_name, email, pwd, salon_id, role_id)
                    if new_emp:
                        QMessageBox.information(self, "Başarılı", "Personel eklendi.")
            
            self.clear_form()
            self.load_employee_data()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İşlem hatası: {e}")