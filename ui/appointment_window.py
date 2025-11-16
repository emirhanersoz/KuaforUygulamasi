import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout,
    QComboBox, QDateEdit, QTimeEdit, QCalendarWidget, QListWidget
)
from PyQt6.QtCore import Qt, QDate

class AppointmentWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Randevu Sistemi")
        
        main_layout = QVBoxLayout()
        
        new_appointment_group = QGroupBox("Yeni Randevu Oluştur")
        form_layout = QFormLayout()
        
        self.salon_combo = QComboBox()
        self.salon_combo.addItems(["Lütfen Salon Seçin", "Merkez Şube", "Anadolu Yakası"])
        
        self.service_combo = QComboBox()
        self.service_combo.addItems(["Lütfen Hizmet Seçin", "Saç Kesimi", "Sakal Tıraşı", "Boya"])
        
        self.employee_combo = QComboBox()
        self.employee_combo.addItems(["Lütfen Personel Seçin", "Ali Veli", "Ayşe Yılmaz"])
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumDate(QDate.currentDate())
        
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        
        form_layout.addRow("Salon:", self.salon_combo)
        form_layout.addRow("Hizmet:", self.service_combo)
        form_layout.addRow("Personel:", self.employee_combo)
        form_layout.addRow("Tarih:", self.date_edit)
        form_layout.addRow("Saat:", self.time_edit)
        
        self.create_appointment_button = QPushButton("Randevu Oluştur")
        form_layout.addWidget(self.create_appointment_button)
        
        new_appointment_group.setLayout(form_layout)
        
        appointment_list_group = QGroupBox("Tüm Randevular")
        list_layout = QVBoxLayout()
        
        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(7)
        self.appointment_table.setHorizontalHeaderLabels([
            "ID", "Müşteri", "Personel", "Hizmet", "Tarih", "Saat", "Durum"
        ])
        self.appointment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.load_appointment_data()
        list_layout.addWidget(self.appointment_table)
        appointment_list_group.setLayout(list_layout)

        main_splitter_layout = QHBoxLayout()
        main_splitter_layout.addWidget(new_appointment_group, 1) 
        main_splitter_layout.addWidget(appointment_list_group, 2) 
        
        main_layout.addLayout(main_splitter_layout)
        self.setLayout(main_layout)

    def load_appointment_data(self):
        sample_data = [
            (1001, "Emirhan Cem", "Ali Veli", "Saç Kesimi", "2025-11-17", "14:00", "Onaylandı"),
            (1002, "Test Müşteri", "Ayşe Yılmaz", "Boya", "2025-11-18", "11:00", "Beklemede"),
        ]
        
        self.appointment_table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, item in enumerate(data):
                self.appointment_table.setItem(row, col, QTableWidgetItem(str(item)))

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = AppointmentWindow()
    window.resize(1000, 600) 
    window.show()
    sys.exit(app.exec())