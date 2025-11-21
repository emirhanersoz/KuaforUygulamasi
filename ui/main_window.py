import sys
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMessageBox, QStatusBar, QStackedWidget
)
from PyQt6.QtCore import Qt

# Tüm UI sayfalarını import ediyoruz
from ui.login_window import LoginWindow
from ui.salon_management_window import SalonManagementWindow
from ui.employee_management_window import EmployeeManagementWindow
from ui.appointment_window import AppointmentWindow
from models.user import User

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Kuaför/Berber Otomasyonu (Test Modu)")
        self.setGeometry(100, 100, 1100, 750)
        
        self.current_user: Optional[User] = None 
        
        self.stacked_widget = QStackedWidget() 
        self.setCentralWidget(self.stacked_widget)
        
        self.status_label = QLabel() 

        self.setup_ui()
        self.add_management_pages()
        self.update_ui_for_role(None) 

        self.admin_menu.menuAction().setVisible(True)
        self.employee_menu.menuAction().setVisible(True)
        self.appointment_menu.menuAction().setVisible(True)
        self.statusBar().showMessage("TEST MODU AKTİF - Tüm menüler açık.")

    def setup_ui(self):
        self.setStatusBar(QStatusBar(self)) 
        self.create_menu_bar()
        
        welcome_page = QWidget()
        welcome_layout = QVBoxLayout(welcome_page)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 20px; color: #333;")
        welcome_layout.addWidget(self.status_label)
        self.stacked_widget.addWidget(welcome_page)

    def add_management_pages(self):
        """Tüm yönetim sayfalarını QStackedWidget'a ekler."""
        self.salon_management_page = SalonManagementWindow(self)
        self.stacked_widget.addWidget(self.salon_management_page)

        self.employee_management_page = EmployeeManagementWindow(self)
        self.stacked_widget.addWidget(self.employee_management_page)

        self.appointment_page = AppointmentWindow(self)
        self.stacked_widget.addWidget(self.appointment_page)
        
        self.page_indices = {
            "welcome": 0,
            "salon_management": 1,
            "employee_management": 2,
            "appointments": 3,
        }

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        self.file_menu = menu_bar.addMenu("Dosya")
        self.admin_menu = menu_bar.addMenu("Yönetim")
        self.employee_menu = menu_bar.addMenu("Çalışan İşlemleri")
        self.appointment_menu = menu_bar.addMenu("Randevular")
        
        self.login_action = self.file_menu.addAction("Giriş Yap (Pasif)")
        self.logout_action = self.file_menu.addAction("Çıkış Yap")
        self.exit_action = self.file_menu.addAction("Uygulamadan Çık")
        
        self.manage_salon_action = self.admin_menu.addAction("Salonları Yönet")
        self.manage_employees_action = self.admin_menu.addAction("Personel Yönet")
        
        self.view_appointments_action = self.appointment_menu.addAction("Randevu Takvimi / Oluştur")

        # self.login_action.triggered.connect(self.open_login_window)
        self.logout_action.triggered.connect(self.handle_logout)
        self.exit_action.triggered.connect(self.close)
        
        self.manage_salon_action.triggered.connect(self.show_salon_management)
        self.manage_employees_action.triggered.connect(self.show_employee_management)
        self.view_appointments_action.triggered.connect(self.show_appointment_window)

        self.update_menu_visibility(False)

    def update_menu_visibility(self, is_logged_in: bool):
        self.login_action.setVisible(not is_logged_in)
        self.logout_action.setVisible(is_logged_in)
        
        if not is_logged_in:
            pass 
        else:

            pass

    def handle_logout(self):
        self.current_user = None
        QMessageBox.information(self, "Bilgi", "Çıkış yapıldı (Test Modu).")
        self.stacked_widget.setCurrentIndex(self.page_indices["welcome"])

    def update_ui_for_role(self, user: Optional[User]):
        if user:
            self.update_menu_visibility(True)
        else:
            self.update_menu_visibility(False)
            self.stacked_widget.setCurrentIndex(self.page_indices["welcome"]) 

    def show_salon_management(self):
        self.stacked_widget.setCurrentIndex(self.page_indices["salon_management"])
        self.statusBar().showMessage("Aktif Ekran: Salon Yönetimi")

    def show_employee_management(self):
        self.stacked_widget.setCurrentIndex(self.page_indices["employee_management"])
        self.statusBar().showMessage("Aktif Ekran: Personel Yönetimi")

    def show_appointment_window(self):
        self.stacked_widget.setCurrentIndex(self.page_indices["appointments"])
        self.statusBar().showMessage("Aktif Ekran: Randevu Sistemi")
            
if __name__ == "__main__":
    try:
        print("Uygulama başlatılıyor...")
        app = QApplication(sys.argv)
        
        print("MainWindow oluşturuluyor...")
        main_window = MainWindow()
        
        print("Pencere gösteriliyor...")
        main_window.show()
        
        print("Uygulama döngüsüne giriliyor...")
        sys.exit(app.exec())
        
    except Exception as e:
        print("\nIs\n!!! UYGULAMA BAŞLATILIRKEN KRİTİK HATA OLUŞTU !!!\nIs")
        import traceback
        traceback.print_exc() 
        print(f"\nHata Mesajı: {e}")
        input("\nKapanmak için Enter'a basın...")