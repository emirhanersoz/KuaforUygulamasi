import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

from services.user_service import authenticate_user
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.user import User

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Kullanıcı Girişi")
        self.setFixedSize(400, 250)
        self.logged_in_user = None 
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("Giriş Yap")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        
        email_label = QLabel("E-posta:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("admin@kuafor.com")
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        
        password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifreniz")
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
        # read inputs
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen e-posta ve şifre alanlarını doldurun.")
            return

        session = None
        try:
            # create session (prefer existing SessionLocal if available)
            try:
                from database.db_connection import SessionLocal
                session = SessionLocal()
            except Exception:
                db_url = getattr(config, 'DATABASE_URL', None)
                if not db_url:
                    QMessageBox.critical(self, "Sistem Hatası", "DB oturumu oluşturulamadı; yapılandırma eksik.")
                    return
                engine = create_engine(db_url)
                SessionLocalFallback = sessionmaker(bind=engine)
                session = SessionLocalFallback()

            # authenticate
            try:
                user = authenticate_user(session, email, password)
            except Exception as e:
                # authentication-level errors should not close the app; show and return
                QMessageBox.critical(self, "Sistem Hatası", f"Giriş sırasında hata: {e}")
                return

            if user:
                self.logged_in_user = user
                QMessageBox.information(self, "Başarılı", f"Hoş geldiniz, {user.first_name}! Rolünüz: {user.role.role_name}")
                # accept the dialog (will return control to caller). Do not call any app-level exit here.
                self.accept()
                return
            else:
                QMessageBox.critical(self, "Hata", "Giriş bilgileri hatalı. Lütfen kontrol edin.")
                return
        except Exception as e:
            # Catch-all: never let an exception bubble out and terminate the app
            QMessageBox.critical(self, "Beklenmeyen Hata", f"Bir hata oluştu: {e}")
            return
        finally:
            if session is not None:
                try:
                    session.close()
                except Exception:
                    pass
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec():
        print("Giriş başarılı.")
    else:
        print("Giriş iptal edildi.")
    sys.exit(app.exec())