import sys
import os
# ensure project root is on sys.path so "from ui.login_window import LoginWindow" works
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMessageBox, QStatusBar, QStackedWidget
)
from PyQt6.QtCore import Qt

from ui.login_window import LoginWindow
from models.user import User

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Kuaför/Berber Otomasyonu")
        self.setGeometry(100, 100, 1000, 700)
        
        self.current_user: Optional[User] = None 
        
        # Farklı ekranları yönetecek widget
        self.stacked_widget = QStackedWidget() 
        self.setCentralWidget(self.stacked_widget)

        self.status_label = QLabel() # Global QLabel nesnesi tanımlanıyor

        self.setup_ui()
        self.update_ui_for_role(None) 

    def setup_ui(self):
        self.setStatusBar(QStatusBar(self)) 
        self.create_menu_bar()
        
        # Giriş yapılmamış ana ekran (Karşılama Sayfası)
        welcome_page = QWidget()
        welcome_layout = QVBoxLayout(welcome_page)
        
        # status_label'ı setup_ui içinde yapılandırıyoruz
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 20px; color: #333;")
        
        welcome_layout.addWidget(self.status_label)
        
        self.stacked_widget.addWidget(welcome_page)
        self.stacked_widget.setCurrentWidget(welcome_page)

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        self.file_menu = menu_bar.addMenu("Dosya")
        self.admin_menu = menu_bar.addMenu("Yönetim")
        self.employee_menu = menu_bar.addMenu("Çalışan İşlemleri")
        
        self.login_action = self.file_menu.addAction("Giriş Yap")
        self.logout_action = self.file_menu.addAction("Çıkış Yap")
        self.exit_action = self.file_menu.addAction("Uygulamadan Çık")
        
        self.login_action.triggered.connect(self.open_login_window)
        self.logout_action.triggered.connect(self.handle_logout)
        self.exit_action.triggered.connect(self.close)
        
        self.manage_salon_action = self.admin_menu.addAction("Salonları Yönet")
        self.manage_employees_action = self.admin_menu.addAction("Personel Yönet")

        self.update_menu_visibility(False)

    def update_menu_visibility(self, is_logged_in: bool):
        self.login_action.setVisible(not is_logged_in)
        self.logout_action.setVisible(is_logged_in)
        
        self.admin_menu.menuAction().setVisible(False)
        self.employee_menu.menuAction().setVisible(False)

        if is_logged_in and self.current_user:
            role_name = self.current_user.role.role_name
            
            if role_name == "Yönetici":
                self.admin_menu.menuAction().setVisible(True)
            elif role_name == "Çalışan":
                self.employee_menu.menuAction().setVisible(True)
            
            # Ana ekran etiketini güncelleme
            self.statusBar().showMessage(f"Giriş yapan: {self.current_user.first_name} | Rol: {role_name}")
            self.status_label.setText(f"Hoş geldiniz, {self.current_user.first_name}! Rolünüz: {role_name}")
            
        else:
            self.statusBar().showMessage("Giriş yapılmadı.")
            self.status_label.setText("Lütfen giriş yapın.") # Çıkış yapıldığında veya başlangıçta

    def open_login_window(self):
        login_dialog = LoginWindow(self) 
        if login_dialog.exec():
            self.current_user = login_dialog.logged_in_user
            self.update_ui_for_role(self.current_user)
        else:
            pass
            
    def handle_logout(self):
        self.current_user = None
        self.update_ui_for_role(None)
        QMessageBox.information(self, "Bilgi", "Başarıyla çıkış yaptınız.")
        
    def update_ui_for_role(self, user: Optional[User]):
        if user:
            self.update_menu_visibility(True)
        else:
            self.update_menu_visibility(False)
            self.stacked_widget.setCurrentIndex(0) 

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())