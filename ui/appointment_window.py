import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout,
    QComboBox, QDateEdit, QMessageBox, QListWidget
)
from PyQt6.QtCore import QDate
from database.db_connection import SessionLocal
from services.salon_service import get_all_salons
from services.appointment_service import create_appointment, get_all_appointments, get_available_slots
from services.employee_service import get_employees_by_salon, get_services_for_employee
from models.user import User

class AppointmentWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Randevu Sistemi")
        
        main_layout = QVBoxLayout()
        
        booking_group = QGroupBox("Randevu Oluştur")
        form_layout = QFormLayout()
        
        self.customer_combo = QComboBox()
        self.salon_combo = QComboBox()
        self.salon_combo.currentIndexChanged.connect(self.on_salon_changed)
        
        self.employee_combo = QComboBox()
        self.employee_combo.currentIndexChanged.connect(self.on_employee_changed)
        
        self.service_combo = QComboBox()
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate())
        
        self.time_slots_list = QListWidget()
        self.time_slots_list.setFixedHeight(100)
        
        self.check_slots_btn = QPushButton("Uygun Saatleri Göster")
        self.check_slots_btn.setStyleSheet("background-color: #FF9800; color: white;")
        self.check_slots_btn.clicked.connect(self.load_available_slots)

        form_layout.addRow("Müşteri:", self.customer_combo)
        form_layout.addRow("Salon:", self.salon_combo)
        form_layout.addRow("Personel:", self.employee_combo)
        form_layout.addRow("Paket/Hizmet:", self.service_combo)
        form_layout.addRow("Tarih:", self.date_edit)
        form_layout.addRow("", self.check_slots_btn)
        form_layout.addRow("Müsait Saatler:", self.time_slots_list)
        
        self.create_btn = QPushButton("Randevuyu Onayla")
        self.create_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        self.create_btn.clicked.connect(self.handle_create_appointment)
        form_layout.addWidget(self.create_btn)
        
        booking_group.setLayout(form_layout)
        
        list_group = QGroupBox("Randevu Listesi")
        list_layout = QVBoxLayout()
        
        self.refresh_btn = QPushButton("Listeyi Yenile")
        self.refresh_btn.clicked.connect(self.load_appointments_table)
        list_layout.addWidget(self.refresh_btn)
        
        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(6)
        self.appointment_table.setHorizontalHeaderLabels(["ID", "Müşteri", "Personel", "Hizmet", "Tarih", "Saat"])
        self.appointment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        list_layout.addWidget(self.appointment_table)
        
        list_group.setLayout(list_layout)

        splitter = QHBoxLayout()
        splitter.addWidget(booking_group, 1) 
        splitter.addWidget(list_group, 2) 
        main_layout.addLayout(splitter)
        self.setLayout(main_layout)
        
        self.load_initial_data()

    def load_initial_data(self):
        self.customer_combo.clear()
        self.salon_combo.clear()
        try:
            with SessionLocal() as db:
                users = db.query(User).all()
                for u in users:
                    self.customer_combo.addItem(f"{u.first_name} {u.last_name}", u.id)
                salons = get_all_salons(db)
                for s in salons:
                    self.salon_combo.addItem(s.name, s.id)
        except Exception as e:
            print(f"Veri yükleme hatası: {e}")

    def on_salon_changed(self):
        salon_id = self.salon_combo.currentData()
        self.employee_combo.clear()
        self.service_combo.clear()
        self.time_slots_list.clear()
        if not salon_id: return
        try:
            with SessionLocal() as db:
                emps = get_employees_by_salon(db, salon_id)
                for e in emps:
                    if e.user:
                        self.employee_combo.addItem(f"{e.user.first_name} {e.user.last_name}", e.id)
        except Exception as e:
            print(f"Personel yükleme hatası: {e}")

    def on_employee_changed(self):
        employee_id = self.employee_combo.currentData()
        salon_id = self.salon_combo.currentData()
        self.service_combo.clear()
        self.time_slots_list.clear()
        if not employee_id or not salon_id: return
        try:
            with SessionLocal() as db:
                services = get_services_for_employee(db, employee_id, salon_id)
                if not services:
                    self.service_combo.addItem("Hizmet yok", None)
                for ss in services:
                    if ss.service:
                        item_text = f"{ss.service.service_name} ({ss.duration_minutes} dk - {ss.price_tl} TL)"
                        self.service_combo.addItem(item_text, {"id": ss.service_id, "duration": ss.duration_minutes})
        except Exception as e:
            print(f"Hizmet yükleme hatası: {e}")

    def load_available_slots(self):
        self.time_slots_list.clear()
        employee_id = self.employee_combo.currentData()
        service_data = self.service_combo.currentData()
        check_date = self.date_edit.date().toPyDate()
        
        if not employee_id or not service_data:
            QMessageBox.warning(self, "Eksik", "Personel ve Hizmet seçiniz.")
            return
            
        try:
            with SessionLocal() as db:
                slots = get_available_slots(db, employee_id, check_date, service_data["duration"])
                if not slots:
                    self.time_slots_list.addItem("Uygun saat yok.")
                else:
                    for slot in slots:
                        self.time_slots_list.addItem(slot)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Saatler hesaplanamadı: {e}")

    def handle_create_appointment(self):
        user_id = self.customer_combo.currentData()
        salon_id = self.salon_combo.currentData()
        employee_id = self.employee_combo.currentData()
        service_data = self.service_combo.currentData()
        check_date = self.date_edit.date().toPyDate()
        
        selected_items = self.time_slots_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Saat seçiniz.")
            return
        
        start_time_str = selected_items[0].text().split(" - ")[0]
        if ":" not in start_time_str: return

        try:
            with SessionLocal() as db:
                create_appointment(db, user_id, salon_id, employee_id, service_data["id"], check_date, start_time_str)
                QMessageBox.information(self, "Başarılı", "Randevu oluşturuldu!")
                self.load_appointments_table()
                self.time_slots_list.clear()
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
                    srv_name = app.service.service_name if app.service else "-"
                    
                    self.appointment_table.setItem(row, 0, QTableWidgetItem(str(app.id)))
                    self.appointment_table.setItem(row, 1, QTableWidgetItem(cust_name))
                    self.appointment_table.setItem(row, 2, QTableWidgetItem(emp_name))
                    self.appointment_table.setItem(row, 3, QTableWidgetItem(srv_name))
                    self.appointment_table.setItem(row, 4, QTableWidgetItem(str(app.appointment_date)))
                    self.appointment_table.setItem(row, 5, QTableWidgetItem(str(app.start_time)))
        except Exception as e:
            print(f"Tablo yükleme hatası: {e}")