from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QFormLayout,
    QComboBox
)
from PyQt6.QtCore import Qt

class EmployeeManagementWindow(QWidget):
    """
    Yöneticilerin çalışanları (personel) yönettiği ekran.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Personel Yönetimi")
        
        main_layout = QVBoxLayout()
        
        # 1. Yeni Çalışan Ekleme Formu
        add_employee_group = QGroupBox("Yeni Personel Kaydı")
        form_layout = QFormLayout()
        
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Bu ComboBox'lar (açılır listeler) ileride veritabanından doldurulacak
        self.salon_combo = QComboBox()
        self.salon_combo.addItems(["Merkez Şube", "Anadolu Yakası"]) # Örnek veri
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Çalışan", "Yönetici"]) # Örnek veri
        
        form_layout.addRow("Adı:", self.first_name_input)
        form_layout.addRow("Soyadı:", self.last_name_input)
        form_layout.addRow("E-posta:", self.email_input)
        form_layout.addRow("Şifre:", self.password_input)
        form_layout.addRow("Atanacak Salon:", self.salon_combo)
        form_layout.addRow("Rolü:", self.role_combo)
        
        self.add_button = QPushButton("Personel Ekle")
        # self.add_button.clicked.connect(self.add_new_employee) # Servisler bağlandığında
        form_layout.addWidget(self.add_button)
        
        add_employee_group.setLayout(form_layout)
        main_layout.addWidget(add_employee_group)
        
        # 2. Mevcut Çalışanları Listeleme Tablosu
        main_layout.addWidget(QLabel("Mevcut Personeller:"))
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(5)
        self.employee_table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "E-posta", "Salon", "Rol"])
        self.employee_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Örnek veri
        self.load_employee_data()
        
        main_layout.addWidget(self.employee_table)
        self.setLayout(main_layout)

    def load_employee_data(self):
        """Örnek çalışan verilerini tabloya yükler."""
        sample_data = [
            (101, "Ali Veli", "ali@kuafor.com", "Merkez Şube", "Çalışan"),
            (102, "Ayşe Yılmaz", "ayse@kuafor.com", "Anadolu Yakası", "Çalışan"),
        ]
        
        self.employee_table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, item in enumerate(data):
                self.employee_table.setItem(row, col, QTableWidgetItem(str(item)))

# Eğer bu pencereyi bağımsız çalıştırmak isterseniz
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = EmployeeManagementWindow()
    window.show()
    sys.exit(app.exec())