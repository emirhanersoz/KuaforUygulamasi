import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Kullanıcı Girişi")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title_label = QLabel("Giriş Yap")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()

        email_label = QLabel("E-posta:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta adresinizi girin")
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        
        password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifrenizi girin")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Giriş Yap")
        self.cancel_button = QPushButton("İptal")
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.login_button.clicked.connect(self.handle_login)
        self.cancel_button.clicked.connect(self.reject)

    def handle_login(self):
        """Giriş butonuna tıklandığında çalışacak fonksiyon."""
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        QMessageBox.information(self, "Bilgi", f"Giriş bilgileri:\nE-posta: {email}\nŞifre: {password}")
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec():
        print("Giriş başarılı.")
    else:
        print("Giriş iptal edildi.")
    sys.exit(app.exec())