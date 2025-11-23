import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QFormLayout
)
from database.db_connection import SessionLocal
from services.user_service import create_user

class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kayıt Ol")
        self.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Yeni Müşteri Kaydı")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        form_layout = QFormLayout()
        
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("Ad:", self.first_name_input)
        form_layout.addRow("Soyad:", self.last_name_input)
        form_layout.addRow("E-posta:", self.email_input)
        form_layout.addRow("Telefon:", self.phone_input)
        form_layout.addRow("Şifre:", self.password_input)
        
        layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        self.register_btn = QPushButton("Kayıt Ol")
        self.cancel_btn = QPushButton("İptal")
        
        self.register_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        
        btn_layout.addWidget(self.register_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.register_btn.clicked.connect(self.handle_register)
        self.cancel_btn.clicked.connect(self.reject)

    def handle_register(self):
        f_name = self.first_name_input.text().strip()
        l_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        pwd = self.password_input.text()

        if not f_name or not l_name or not email or not pwd:
            QMessageBox.warning(self, "Eksik", "Lütfen tüm zorunlu alanları doldurun.")
            return

        try:
            with SessionLocal() as db:
                new_user = create_user(db, f_name, l_name, email, pwd, "Müşteri", phone)
                if new_user:
                    QMessageBox.information(self, "Başarılı", "Kayıt başarıyla oluşturuldu!\nŞimdi giriş yapabilirsiniz.")
                    self.accept()
                else:
                    QMessageBox.warning(self, "Hata", "Kayıt yapılamadı. Bu e-posta zaten kullanılıyor olabilir.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt sırasında hata oluştu: {e}")