import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout,
    QComboBox, QDateEdit, QTimeEdit, QMessageBox
)
from PyQt6.QtCore import QDate, QTime
from database.db_connection import SessionLocal
from services.salon_service import get_all_salons
from services.appointment_service import create_appointment, get_all_appointments
from services.employee_service import get_employees_by_salon
from models.user import User
from models.salon_service import SalonService

class AppointmentWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Randevu Sistemi")
        
        main_layout = QVBoxLayout()
        
        new_appointment_group = QGroupBox("Yeni Randevu Oluştur")
        form_layout = QFormLayout()
        
        self.customer_combo = QComboBox()
        self.salon_combo = QComboBox()
        self.salon_combo.currentIndexChanged.connect(self.on_salon_changed)
        self.service_combo = QComboBox()
        self.employee_combo = QComboBox()
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(9, 0))
        
        form_layout.addRow("Müşteri:", self.customer_combo)
        form_layout.addRow("Salon:", self.salon_combo)
        form_layout.addRow("Hizmet:", self.service_combo)
        form_layout.addRow("Personel:", self.employee_combo)
        form_layout.addRow("Tarih:", self.date_edit)
        form_layout.addRow("Saat:", self.time_edit)
        
        self.create_btn = QPushButton("Randevu Oluştur")
        self.create_btn.clicked.connect(self.handle_create_appointment)
        form_layout.addWidget(self.create_btn)
        
        new_appointment_group.setLayout(form_layout)
        
        appointment_list_group = QGroupBox("Tüm Randevular")
        list_layout = QVBoxLayout()

        self.refresh_btn = QPushButton("Verileri Getir / Yenile")
        self.refresh_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        self.refresh_btn.clicked.connect(self.load_all_data)
        list_layout.addWidget(self.refresh_btn)
        
        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(6)
        self.appointment_table.setHorizontalHeaderLabels([
            "ID", "Müşteri", "Personel", "Hizmet", "Tarih", "Saat"
        ])
        self.appointment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        list_layout.addWidget(self.appointment_table)
        appointment_list_group.setLayout(list_layout)

        splitter = QHBoxLayout()
        splitter.addWidget(new_appointment_group, 1) 
        splitter.addWidget(appointment_list_group, 2) 
        main_layout.addLayout(splitter)
        self.setLayout(main_layout)
        
    def load_all_data(self):
        self.load_initial_data()
        self.load_appointments_table()
        QMessageBox.information(self, "Bilgi", "Randevu verileri yüklendi.")

    def load_initial_data(self):
        self.customer_combo.clear()
        self.salon_combo.clear()
        
        try:
            with SessionLocal() as db:
                users = db.query(User).all()
                for u in users:
                    self.customer_combo.addItem(f"{u.first_name} {u.last_name} ({u.email})", u.id)
                
                salons = get_all_salons(db)
                for s in salons:
                    self.salon_combo.addItem(s.name, s.id)
        except Exception as e:
            print(f"Müşteri/Salon listesi yüklenemedi: {e}")

    def on_salon_changed(self):
        salon_id = self.salon_combo.currentData()
        if not salon_id:
            return
            
        self.employee_combo.clear()
        self.service_combo.clear()
        
        try:
            with SessionLocal() as db:
                emps = get_employees_by_salon(db, salon_id)
                for e in emps:
                    if e.user:
                        self.employee_combo.addItem(f"{e.user.first_name} {e.user.last_name}", e.id)
                
                salon_services = db.query(SalonService).filter(SalonService.salon_id == salon_id).all()
                for ss in salon_services:
                    if ss.service:
                         self.service_combo.addItem(f"{ss.service.service_name} ({ss.price_tl} TL)", ss.id)
        except Exception as e:
            print(f"Salon detayları çekilemedi: {e}")

    def handle_create_appointment(self):
        user_id = self.customer_combo.currentData()
        salon_id = self.salon_combo.currentData()
        salon_service_id = self.service_combo.currentData()
        employee_id = self.employee_combo.currentData()
        
        q_date = self.date_edit.date().toPyDate()
        q_time = self.time_edit.time().toPyTime()
        
        from datetime import datetime, timedelta
        dummy_end = (datetime.combine(q_date, q_time) + timedelta(hours=1)).time()

        if not all([user_id, salon_id, salon_service_id, employee_id]):
            QMessageBox.warning(self, "Eksik", "Lütfen tüm seçimleri yapınız.")
            return

        try:
            with SessionLocal() as db:
                create_appointment(
                    db, user_id, salon_id, employee_id, salon_service_id, 
                    q_date, q_time, dummy_end
                )
                QMessageBox.information(self, "Başarılı", "Randevu oluşturuldu!")
                self.load_appointments_table()
        except Exception as e:
             QMessageBox.critical(self, "Hata", f"Randevu oluşturulamadı: {e}")

    def load_appointments_table(self):
        self.appointment_table.setRowCount(0)
        try:
            with SessionLocal() as db:
                apps = get_all_appointments(db)
                self.appointment_table.setRowCount(len(apps))
                for row, app in enumerate(apps):
                    cust_name = f"{app.user.first_name} {app.user.last_name}" if app.user else "?"
                    emp_name = f"{app.employee.user.first_name}" if (app.employee and app.employee.user) else "?"
                    srv_name = "-"
                    if app.salon_service and app.salon_service.service:
                        srv_name = app.salon_service.service.service_name
                    
                    self.appointment_table.setItem(row, 0, QTableWidgetItem(str(app.id)))
                    self.appointment_table.setItem(row, 1, QTableWidgetItem(cust_name))
                    self.appointment_table.setItem(row, 2, QTableWidgetItem(emp_name))
                    self.appointment_table.setItem(row, 3, QTableWidgetItem(srv_name))
                    self.appointment_table.setItem(row, 4, QTableWidgetItem(str(app.appointment_date)))
                    self.appointment_table.setItem(row, 5, QTableWidgetItem(str(app.start_time)))
        except Exception as e:
            print(f"Tablo yükleme hatası: {e}")