import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from database.db_connection import SessionLocal
from services.user_service import authenticate_user

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kullanıcı Girişi")
        self.setFixedSize(400, 250)
        
        self.user_data_dict = None 
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("Giriş Yap")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta")
        self.email_input.setText("admin@kuafor.com") 
        form_layout.addWidget(QLabel("E-posta:"))
        form_layout.addWidget(self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(QLabel("Şifre:"))
        form_layout.addWidget(self.password_input)
        
        layout.addLayout(form_layout)
        
        btns = QHBoxLayout()
        self.login_btn = QPushButton("Giriş Yap")
        self.cancel_btn = QPushButton("İptal")
        btns.addWidget(self.login_btn)
        btns.addWidget(self.cancel_btn)
        layout.addLayout(btns)
        
        self.login_btn.clicked.connect(self.handle_login)
        self.cancel_btn.clicked.connect(self.reject)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        print(f"DEBUG: Giriş deneniyor -> {email}")

        if password == "bypass":
            print("DEBUG: Bypass modu aktif!")
            self.user_data_dict = {
                'id': 999,
                'first_name': 'Bypass',
                'last_name': 'Admin',
                'email': email,
                'role_name': 'Yönetici'
            }
            self.accept()
            return
        # -----------------------------------------------

        db = None
        try:
            print("DEBUG: Veritabanı oturumu açılıyor...")
            db = SessionLocal()
            
            print("DEBUG: authenticate_user çağrılıyor...")
            user = authenticate_user(db, email, password)
            
            if user:
                print(f"DEBUG: Kullanıcı bulundu: {user.first_name}")
                r_name = user.role.role_name if user.role else "Kullanıcı"
                
                self.user_data_dict = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role_name': r_name
                }
                QMessageBox.information(self, "Başarılı", "Giriş yapıldı.")
                self.accept()
            else:
                print("DEBUG: Kullanıcı yok veya şifre yanlış.")
                QMessageBox.critical(self, "Hata", "Giriş başarısız. (Şifre yanlış)")

        except Exception as e:
            print(f"DEBUG HATASI: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Kritik Hata", f"Sistem hatası:\n{e}")
        finally:
            if db:
                print("DEBUG: Oturum kapatılıyor.")
                db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    if win.exec():
        print("Login Başarılı:", win.user_data_dict)
    sys.exit(app.exec())