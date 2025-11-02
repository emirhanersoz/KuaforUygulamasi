import sys
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMessageBox, QStatusBar, QStackedWidget
)
from PyQt6.QtCore import Qt

# Login'i şimdilik import etmiyoruz, hata veriyordu.
# from ui.login_window import LoginWindow 
from ui.salon_management_window import SalonManagementWindow
from ui.employee_management_window import EmployeeManagementWindow # YENİ EKRAN
from models.user import User

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Kuaför/Berber Otomasyonu (Test Modu)")
        self.setGeometry(100, 100, 1000, 700)
        
        self.current_user: Optional[User] = None 
        
        self.stacked_widget = QStackedWidget() 
        self.setCentralWidget(self.stacked_widget)
        
        self.status_label = QLabel() 

        self.setup_ui()
        self.add_management_pages()
        self.update_ui_for_role(None) 
        
        # --- GEÇİCİ TEST KODU ---
        # Login ekranı çalışmadığı için, menüleri manuel olarak görünür yapıyoruz.
        print("GEÇİCİ TEST MODU: Yönetim menüsü manuel olarak görünür yapıldı.")
        self.admin_menu.menuAction().setVisible(True)
        self.statusBar().showMessage("TEST MODU AKTİF - Giriş yapılmadı.")
        # --- TEST KODU BİTİŞİ ---

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
        """Yönetim sayfalarını QStackedWidget'a ekler."""
        
        # Index 1: Salon Yönetimi Sayfası
        self.salon_management_page = SalonManagementWindow(self)
        self.stacked_widget.addWidget(self.salon_management_page)
        
        # Index 2: Personel Yönetimi Sayfası
        self.employee_management_page = EmployeeManagementWindow(self)
        self.stacked_widget.addWidget(self.employee_management_page)
        
        self.page_indices = {
            "welcome": 0,
            "salon_management": 1,
            "employee_management": 2, # YENİ EKLENDİ
        }

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        self.file_menu = menu_bar.addMenu("Dosya")
        self.admin_menu = menu_bar.addMenu("Yönetim")
        self.employee_menu = menu_bar.addMenu("Çalışan İşlemleri")
        
        self.login_action = self.file_menu.addAction("Giriş Yap (Devre Dışı)")
        self.logout_action = self.file_menu.addAction("Çıkış Yap")
        self.exit_action = self.file_menu.addAction("Uygulamadan Çık")
        
        self.manage_salon_action = self.admin_menu.addAction("Salonları Yönet")
        self.manage_employees_action = self.admin_menu.addAction("Personel Yönet")

        # self.login_action.triggered.connect(self.open_login_window) # Test için kapalı
        self.logout_action.triggered.connect(self.handle_logout)
        self.exit_action.triggered.connect(self.close)
        
        self.manage_salon_action.triggered.connect(self.show_salon_management)
        self.manage_employees_action.triggered.connect(self.show_employee_management) # YENİ BAĞLANTI

        self.update_menu_visibility(False)

    def update_menu_visibility(self, is_logged_in: bool):
        # Bu fonksiyon şimdilik login ekranı olmadığı için tam çalışmayacak,
        # ancak çıkış yapma (handle_logout) fonksiyonu için gerekli.
        self.login_action.setVisible(not is_logged_in)
        self.logout_action.setVisible(is_logged_in)
        
        self.admin_menu.menuAction().setVisible(False)
        self.employee_menu.menuAction().setVisible(False)

        if is_logged_in and self.current_user:
            # Burası normalde giriş yapılınca çalışacak
            # ...
            pass
        else:
            self.statusBar().showMessage("Giriş yapılmadı.")
            self.status_label.setText("Lütfen giriş yapın.")

    # def open_login_window(self):
    #     # Bu fonksiyon login hatası nedeniyle geçici olarak devre dışı
    #     QMessageBox.warning(self, "Devre Dışı", "Login fonksiyonu şu anda geliştirme aşamasındadır.")
    #     pass
            
    def handle_logout(self):
        """Çıkış yapma işlemini gerçekleştirir (Test modunu sıfırlar)."""
        self.current_user = None
        self.update_ui_for_role(None)
        
        # Test için eklediğimiz menüleri tekrar gizle
        self.admin_menu.menuAction().setVisible(False)
        
        QMessageBox.information(self, "Bilgi", "Test modundan çıkıldı (Sıfırlandı).")
        
    def update_ui_for_role(self, user: Optional[User]):
        """Kullanıcıya göre arayüzü ayarlar."""
        if user:
            self.update_menu_visibility(True)
        else:
            self.update_menu_visibility(False)
            self.stacked_widget.setCurrentIndex(self.page_indices["welcome"]) 

    def show_salon_management(self):
        """Salon Yönetimi sayfasını gösterir."""
        self.stacked_widget.setCurrentIndex(self.page_indices["salon_management"])
        self.statusBar().showMessage("Aktif Ekran: Salon Yönetimi")

    def show_employee_management(self):
        """Personel Yönetimi sayfasını gösterir."""
        self.stacked_widget.setCurrentIndex(self.page_indices["employee_management"])
        self.statusBar().showMessage("Aktif Ekran: Personel Yönetimi")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())