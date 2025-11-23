import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout, 
    QTimeEdit, QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QTime
from database.db_connection import SessionLocal
from services.employee_service import (
    set_employee_availability, get_employee_appointments, 
    update_appointment_status, add_service_to_employee
)
from models.employee import Employee

class EmployeeDashboard(QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.employee_id = None
        self.setWindowTitle(f"Çalışan Paneli - {current_user.first_name} {current_user.last_name}")
        self.resize(900, 600)

        self.find_employee_id()
        
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        
        self.appointments_tab = QWidget()
        self.setup_appointments_tab()
        self.tabs.addTab(self.appointments_tab, "Randevu İstekleri")
        
        self.availability_tab = QWidget()
        self.setup_availability_tab()
        self.tabs.addTab(self.availability_tab, "Çalışma Saatlerim")

        self.services_tab = QWidget()
        self.setup_services_tab()
        self.tabs.addTab(self.services_tab, "Hizmet ve Fiyatlarım")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def find_employee_id(self):
        try:
            with SessionLocal() as db:
                emp = db.query(Employee).filter(Employee.user_id == self.current_user.id).first()
                if emp:
                    self.employee_id = emp.id
                else:
                    QMessageBox.critical(self, "Hata", "Çalışan kaydınız bulunamadı!")
                    self.close()
        except Exception as e:
            print(f"ID Bulma Hatası: {e}")

    def setup_appointments_tab(self):
        layout = QVBoxLayout(self.appointments_tab)
        
        refresh_btn = QPushButton("Listeyi Yenile")
        refresh_btn.clicked.connect(self.load_appointments)
        layout.addWidget(refresh_btn)
        
        self.app_table = QTableWidget()
        self.app_table.setColumnCount(6)
        self.app_table.setHorizontalHeaderLabels(["Müşteri", "Tarih", "Saat", "Durum", "Onayla", "Reddet"])
        self.app_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.app_table)
        
        self.load_appointments()

    def load_appointments(self):
        if not self.employee_id: return
        self.app_table.setRowCount(0)
        
        try:
            with SessionLocal() as db:
                apps = get_employee_appointments(db, self.employee_id)
                self.app_table.setRowCount(len(apps))
                
                for row, app in enumerate(apps):
                    cust_name = f"{app.user.first_name} {app.user.last_name}"
                    status = "Bekliyor"
                    if app.is_confirmed: status = "Onaylı"
                    if app.is_cancelled: status = "Reddedildi"
                    
                    self.app_table.setItem(row, 0, QTableWidgetItem(cust_name))
                    self.app_table.setItem(row, 1, QTableWidgetItem(str(app.appointment_date)))
                    self.app_table.setItem(row, 2, QTableWidgetItem(str(app.start_time)))
                    self.app_table.setItem(row, 3, QTableWidgetItem(status))

                    if not app.is_confirmed and not app.is_cancelled:
                        btn_ok = QPushButton("Onayla")
                        btn_ok.setStyleSheet("background-color: #4CAF50; color: white;")
                        btn_ok.clicked.connect(lambda ch, aid=app.id: self.change_status(aid, True))
                        self.app_table.setCellWidget(row, 4, btn_ok)
                        
                        btn_no = QPushButton("Reddet")
                        btn_no.setStyleSheet("background-color: #f44336; color: white;")
                        btn_no.clicked.connect(lambda ch, aid=app.id: self.change_status(aid, False))
                        self.app_table.setCellWidget(row, 5, btn_no)
        except Exception as e:
            print(f"Randevu yükleme hatası: {e}")

    def change_status(self, app_id, confirmed):
        try:
            with SessionLocal() as db:
                update_appointment_status(db, app_id, confirmed)
                QMessageBox.information(self, "Bilgi", "Durum güncellendi.")
                self.load_appointments()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def setup_availability_tab(self):
        layout = QVBoxLayout(self.availability_tab)
        
        form_layout = QFormLayout()
        
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])
        
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setTime(QTime(9, 0))
        
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setTime(QTime(18, 0))
        
        form_layout.addRow("Gün Seç:", self.day_combo)
        form_layout.addRow("Başlangıç Saati:", self.start_time)
        form_layout.addRow("Bitiş Saati:", self.end_time)
        
        save_btn = QPushButton("Saati Kaydet")
        save_btn.clicked.connect(self.save_availability)
        
        layout.addLayout(form_layout)
        layout.addWidget(save_btn)
        layout.addStretch()

    def save_availability(self):
        day_idx = self.day_combo.currentIndex()
        start = self.start_time.time().toPyTime()
        end = self.end_time.time().toPyTime()
        
        if not self.employee_id: return
        
        try:
            with SessionLocal() as db:
                set_employee_availability(db, self.employee_id, day_idx, start, end)
                QMessageBox.information(self, "Başarılı", f"{self.day_combo.currentText()} günü saatleri güncellendi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def setup_services_tab(self):
        layout = QVBoxLayout(self.services_tab)
        
        form_layout = QFormLayout()
        self.srv_name_input = QLineEdit()
        self.srv_name_input.setPlaceholderText("Örn: Saç Kesimi")
        
        self.srv_duration = QSpinBox()
        self.srv_duration.setRange(5, 480)
        self.srv_duration.setValue(30)
        self.srv_duration.setSuffix(" dk")
        
        self.srv_price = QDoubleSpinBox()
        self.srv_price.setRange(0, 10000)
        self.srv_price.setValue(100)
        self.srv_price.setSuffix(" TL")
        
        form_layout.addRow("Hizmet Adı:", self.srv_name_input)
        form_layout.addRow("Süre:", self.srv_duration)
        form_layout.addRow("Ücret:", self.srv_price)
        
        add_btn = QPushButton("Hizmeti Ekle / Güncelle")
        add_btn.clicked.connect(self.add_service)
        
        layout.addLayout(form_layout)
        layout.addWidget(add_btn)
        layout.addStretch()
        
    def add_service(self):
        name = self.srv_name_input.text()
        duration = self.srv_duration.value()
        price = self.srv_price.value()
        
        if not name: return
        
        try:
            with SessionLocal() as db:
                add_service_to_employee(db, self.employee_id, name, duration, price)
                QMessageBox.information(self, "Başarılı", "Hizmet listenize eklendi.")
        except Exception as e:
             QMessageBox.critical(self, "Hata", str(e))