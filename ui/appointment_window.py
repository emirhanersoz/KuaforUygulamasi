import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout,
    QComboBox, QDateEdit, QMessageBox, QListWidget
)
from PyQt6.QtCore import QDate, Qt 
from database.db_connection import SessionLocal
from services.salon_service import get_all_salons
from services.appointment_service import (
    create_appointment, get_all_appointments, get_available_slots, 
    get_user_appointments, cancel_appointment
)
from services.employee_service import get_employees_by_salon, get_services_for_employee
from models.user import User

class AppointmentWindow(QWidget):
    def __init__(self, current_user=None, parent=None):
        super().__init__(parent)
        self.current_user = current_user
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
        self.service_combo.currentIndexChanged.connect(self.try_auto_load_slots)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.try_auto_load_slots)
        
        self.time_slots_list = QListWidget()
        self.time_slots_list.setFixedHeight(120)
        
        form_layout.addRow("Müşteri:", self.customer_combo)
        form_layout.addRow("Salon:", self.salon_combo)
        form_layout.addRow("Personel:", self.employee_combo)
        form_layout.addRow("Hizmet:", self.service_combo)
        form_layout.addRow("Tarih:", self.date_edit)
        form_layout.addRow("Müsait Saatler:", self.time_slots_list)
        
        self.create_btn = QPushButton("Randevuyu Onayla")
        self.create_btn.clicked.connect(self.handle_create_appointment)
        form_layout.addWidget(self.create_btn)
        
        booking_group.setLayout(form_layout)
        
        list_group = QGroupBox("Randevularım")
        list_layout = QVBoxLayout()
        
        self.refresh_btn = QPushButton("Listeyi Yenile")
        self.refresh_btn.clicked.connect(self.load_appointments_table)
        list_layout.addWidget(self.refresh_btn)
        
        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(8)
        self.appointment_table.setHorizontalHeaderLabels(["ID", "Müşteri", "Personel", "Hizmet", "Tarih", "Saat", "Durum", "İşlem"])
        self.appointment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.appointment_table.setColumnHidden(0, True) # ID Gizli
        
        list_layout.addWidget(self.appointment_table)
        list_group.setLayout(list_layout)

        splitter = QHBoxLayout()
        splitter.addWidget(booking_group, 1) 
        splitter.addWidget(list_group, 2) 
        main_layout.addLayout(splitter)
        self.setLayout(main_layout)
        
        self.load_initial_data()
        self.configure_for_role()

    def configure_for_role(self):
        if not self.current_user: return
        
        if hasattr(self.current_user, 'role_id') and self.current_user.role_id == 1:
            self.customer_combo.clear()
            self.customer_combo.addItem(f"{self.current_user.first_name} {self.current_user.last_name}", self.current_user.id)
            self.customer_combo.setEnabled(False)
            self.appointment_table.setHorizontalHeaderItem(1, QTableWidgetItem("Salon"))
        else:
            self.customer_combo.setEnabled(True)
            self.appointment_table.setHorizontalHeaderItem(1, QTableWidgetItem("Müşteri"))
            
        self.load_appointments_table()

    def load_initial_data(self):
        self.customer_combo.clear()
        self.salon_combo.clear()
        try:
            with SessionLocal() as db:
                if not self.current_user or not hasattr(self.current_user, 'role_id') or self.current_user.role_id != 1:
                    users = db.query(User).all()
                    
                    current_user_index = 0
                    for i, u in enumerate(users):
                        role_name = u.role.role_name if u.role else ""
                        display_text = f"{u.first_name} {u.last_name} ({role_name})"
                        
                        self.customer_combo.addItem(display_text, u.id)

                        if self.current_user and u.id == self.current_user.id:
                            current_user_index = i

                    self.customer_combo.setCurrentIndex(current_user_index)
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

    def try_auto_load_slots(self):
        employee_id = self.employee_combo.currentData()
        service_data = self.service_combo.currentData()
        if not employee_id or not service_data: return
        self.load_available_slots()

    def load_available_slots(self):
        self.time_slots_list.clear()
        employee_id = self.employee_combo.currentData()
        service_data = self.service_combo.currentData()
        check_date = self.date_edit.date().toPyDate()
        
        if not employee_id or not service_data: return
            
        try:
            with SessionLocal() as db:
                slots = get_available_slots(db, employee_id, check_date, service_data["duration"])
                if not slots:
                    self.time_slots_list.addItem("Uygun saat yok.")
                else:
                    for slot in slots:
                        self.time_slots_list.addItem(slot)
        except Exception as e:
            print(f"Saat hesaplama hatası: {e}")

    def handle_create_appointment(self):
        if hasattr(self.current_user, 'role_id') and self.current_user.role_id == 1:
            user_id = self.current_user.id
        else:
            user_id = self.customer_combo.currentData()

        salon_id = self.salon_combo.currentData()
        employee_id = self.employee_combo.currentData()
        service_data = self.service_combo.currentData()
        check_date = self.date_edit.date().toPyDate()
        
        selected_items = self.time_slots_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir saat seçiniz.")
            return
        
        slot_text = selected_items[0].text()
        if "yok" in slot_text: return
        
        start_time_str = slot_text.split(" - ")[0]

        try:
            with SessionLocal() as db:
                create_appointment(db, user_id, salon_id, employee_id, service_data["id"], check_date, start_time_str)
                QMessageBox.information(self, "Başarılı", "Randevunuz oluşturuldu!\nDurum: Onay Bekliyor.")
                self.load_appointments_table()
                self.time_slots_list.clear()
                self.try_auto_load_slots()
        except Exception as e:
             QMessageBox.critical(self, "Hata", f"Randevu oluşturulamadı: {e}")

    def load_appointments_table(self):
        self.appointment_table.setRowCount(0)
        if not self.current_user: return

        try:
            with SessionLocal() as db:
                is_customer = False
                if hasattr(self.current_user, 'role_id') and self.current_user.role_id == 1:
                    is_customer = True
                    apps = get_user_appointments(db, self.current_user.id)
                else:
                    apps = get_all_appointments(db)

                self.appointment_table.setRowCount(len(apps))
                for row, app in enumerate(apps):
                    if is_customer:
                        col1_text = app.salon.name if app.salon else "Bilinmiyor"
                    else:
                        col1_text = f"{app.user.first_name} {app.user.last_name}" if app.user else "?"

                    if app.employee and app.employee.user:
                        emp_name = f"{app.employee.user.first_name} {app.employee.user.last_name}"
                    else:
                        emp_name = "?"
                    
                    srv_name = app.service.service_name if app.service else "-"
                    
                    status_text = "Onay Bekliyor"
                    status_color = "#FF9800" 
                    if app.is_confirmed: 
                        status_text = "Onaylandı"
                        status_color = "#4CAF50"
                    if app.is_cancelled: 
                        status_text = "İptal Edildi"
                        status_color = "#F44336"

                    self.appointment_table.setItem(row, 0, QTableWidgetItem(str(app.id)))
                    self.appointment_table.setItem(row, 1, QTableWidgetItem(col1_text))
                    self.appointment_table.setItem(row, 2, QTableWidgetItem(emp_name))
                    self.appointment_table.setItem(row, 3, QTableWidgetItem(srv_name))
                    self.appointment_table.setItem(row, 4, QTableWidgetItem(str(app.appointment_date)))
                    self.appointment_table.setItem(row, 5, QTableWidgetItem(str(app.start_time)))
                    
                    status_item = QTableWidgetItem(status_text)
                    status_item.setForeground(Qt.GlobalColor.black)
                    status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.appointment_table.setItem(row, 6, status_item)

                    if not app.is_cancelled:
                        btn_cancel = QPushButton("İptal Et")
                        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
                        btn_cancel.setStyleSheet("""
                            QPushButton { background-color: #ef5350; color: white; border-radius: 4px; padding: 2px; font-weight: bold; }
                            QPushButton:hover { background-color: #e53935; }
                        """)
                        btn_cancel.clicked.connect(lambda ch, aid=app.id: self.cancel_my_appointment(aid))
                        
                        container = QWidget()
                        layout = QHBoxLayout(container)
                        layout.setContentsMargins(5, 2, 5, 2)
                        layout.addWidget(btn_cancel)
                        self.appointment_table.setCellWidget(row, 7, container)
                    else:
                        lbl = QLabel("-")
                        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.appointment_table.setCellWidget(row, 7, lbl)

        except Exception as e:
            print(f"Tablo yükleme hatası: {e}")

    def cancel_my_appointment(self, app_id):
        reply = QMessageBox.question(self, "İptal", "Randevuyu iptal etmek istediğinize emin misiniz?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with SessionLocal() as db:
                    if cancel_appointment(db, app_id):
                        QMessageBox.information(self, "Bilgi", "Randevu iptal edildi.")
                        self.load_appointments_table()
                        self.try_auto_load_slots()
                    else:
                        QMessageBox.warning(self, "Hata", "İptal edilemedi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", str(e))