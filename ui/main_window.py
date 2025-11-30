import sys
import traceback
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox, QStatusBar, QStackedWidget
)
from PyQt6.QtCore import Qt

try:
    from ui.styles import MODERN_THEME
except ImportError:
    MODERN_THEME = ""

try:
    from ui.login_window import LoginWindow
    from ui.register_window import RegisterWindow
    from ui.salon_management_window import SalonManagementWindow
    from ui.employee_management_window import EmployeeManagementWindow
    from ui.user_management_window import UserManagementWindow
    from ui.appointment_window import AppointmentWindow
except Exception as e:
    print(f"Import Hatası (Ana Modüller): {e}")

class SafeUser:
    def __init__(self, data_dict):
        self.id = data_dict.get('id')
        self.first_name = data_dict.get('first_name')
        self.last_name = data_dict.get('last_name')
        self.email = data_dict.get('email')
        self.role_id = data_dict.get('role_id')
        role_name = data_dict.get('role_name', 'Tanımsız')
        self.role = type('Role', (), {'role_name': role_name, 'id': self.role_id})()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kuaför Otomasyonu")
        self.setGeometry(100, 100, 1100, 750)
        
        self.current_user = None 
        self.stacked_widget = QStackedWidget() 
        self.setCentralWidget(self.stacked_widget)
        self.status_label = QLabel() 

        self.page_indices = {
            "welcome": 0,
            "salon_management": 1,
            "employee_management": 2,
            "user_management": 3,
            "appointments": 4,
        }

        self.setup_ui()
        self.add_management_pages()
        self.update_ui_for_role(None) 
        self.statusBar().showMessage("Sistem Hazır.")

    def setup_ui(self):
        self.setStatusBar(QStatusBar(self)) 
        self.create_menu_bar()
        
        self.welcome_page = QWidget()
        welcome_layout = QVBoxLayout(self.welcome_page)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.setSpacing(20) 

        self.logo_label = QLabel("✂️💈")
        self.logo_label.setStyleSheet("font-size: 80px; background: transparent;")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = QLabel("Güzellik & Bakım Merkezi")
        self.title_label.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #880e4f;
            margin-bottom: 10px;
            background: transparent;
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Lütfen giriş yapınız.")
        self.status_label.setStyleSheet("font-size: 18px; color: #5d4037; background: transparent;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)
        self.buttons_layout.setSpacing(20)
        self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_login_big = QPushButton("Giriş Yap")
        self.btn_login_big.setFixedSize(150, 50)
        self.btn_login_big.setStyleSheet("font-size: 16px;")
        self.btn_login_big.clicked.connect(self.open_login_window)
        
        self.btn_register_big = QPushButton("Kayıt Ol")
        self.btn_register_big.setFixedSize(150, 50)
        self.btn_register_big.setStyleSheet("font-size: 16px; background-color: #ffffff; color: #ec407a; border: 2px solid #ec407a;")
        self.btn_register_big.clicked.connect(self.open_register_window)
        
        self.buttons_layout.addWidget(self.btn_login_big)
        self.buttons_layout.addWidget(self.btn_register_big)

        welcome_layout.addStretch()
        welcome_layout.addWidget(self.logo_label)
        welcome_layout.addWidget(self.title_label)
        welcome_layout.addWidget(self.status_label)
        welcome_layout.addWidget(self.buttons_widget)
        welcome_layout.addStretch()

        slogan = QLabel("Stiliniz, İmzanızdır.")
        slogan.setStyleSheet("font-style: italic; color: #9e9e9e; margin-bottom: 20px; background: transparent;")
        slogan.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(slogan)

        self.stacked_widget.addWidget(self.welcome_page)

    def add_management_pages(self):
        try:
            self.salon_management_page = SalonManagementWindow(self)
            self.stacked_widget.addWidget(self.salon_management_page)
        except Exception: self.stacked_widget.addWidget(QLabel("Salon Sayfası Yüklenemedi"))

        try:
            self.employee_management_page = EmployeeManagementWindow(self)
            self.stacked_widget.addWidget(self.employee_management_page)
        except Exception: self.stacked_widget.addWidget(QLabel("Personel Sayfası Yüklenemedi"))
        
        try:
            self.user_management_page = UserManagementWindow(self)
            self.stacked_widget.addWidget(self.user_management_page)
        except Exception: self.stacked_widget.addWidget(QLabel("Kullanıcı Sayfası Yüklenemedi"))

        try:
            self.appointment_page = AppointmentWindow(self.current_user, self)
            self.stacked_widget.addWidget(self.appointment_page)
        except Exception: self.stacked_widget.addWidget(QLabel("Randevu Sayfası Yüklenemedi"))

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        self.file_menu = menu_bar.addMenu("Dosya")
        self.admin_menu = menu_bar.addMenu("Yönetim")
        self.appointment_menu = menu_bar.addMenu("Randevular")
        
        self.login_action = self.file_menu.addAction("Giriş Yap")
        self.register_action = self.file_menu.addAction("Kayıt Ol")
        self.logout_action = self.file_menu.addAction("Çıkış Yap")
        
        self.manage_salon_action = self.admin_menu.addAction("Salonları Yönet")
        self.manage_employees_action = self.admin_menu.addAction("Personelleri Yönet")
        self.manage_users_action = self.admin_menu.addAction("Tüm Kullanıcıları Yönet")
        self.manage_appointments_action = self.admin_menu.addAction("Randevuları Yönet")
        
        self.view_appointments_action = self.appointment_menu.addAction("Randevu Takvimi")

        self.login_action.triggered.connect(self.open_login_window)
        self.register_action.triggered.connect(self.open_register_window)
        self.logout_action.triggered.connect(self.handle_logout)
        
        self.manage_salon_action.triggered.connect(self.show_salon_management)
        self.manage_employees_action.triggered.connect(self.show_employee_management)
        self.manage_users_action.triggered.connect(self.show_user_management)
        self.manage_appointments_action.triggered.connect(self.show_appointment_window)
        self.view_appointments_action.triggered.connect(self.show_appointment_window)

        self.employee_menu = menu_bar.addMenu("Personel Paneli")
        self.open_emp_dashboard = self.employee_menu.addAction("Çalışma Masam")
        self.open_emp_dashboard.triggered.connect(self.show_employee_dashboard)

        self.update_menu_visibility(False)

    def open_login_window(self):
        try:
            login_dialog = LoginWindow(self)
            if login_dialog.exec(): 
                data = login_dialog.user_data_dict
                if data:
                    self.current_user = SafeUser(data)
                    self.update_ui_for_role(self.current_user)
        except Exception as e:
            print(f"Login Akış Hatası: {e}")
            traceback.print_exc()

    def open_register_window(self):
        try:
            reg_dialog = RegisterWindow(self)
            reg_dialog.exec()
        except Exception as e:
            print(f"Kayıt Hatası: {e}")

    def update_menu_visibility(self, is_logged_in: bool):
        self.login_action.setVisible(not is_logged_in)
        self.register_action.setVisible(not is_logged_in)
        self.logout_action.setVisible(is_logged_in)
        
        show_admin_menu = False
        show_appointment_menu = False
        show_employee_menu = False
        
        if is_logged_in and self.current_user:
            rid = self.current_user.role_id
            
            if rid == 3:
                show_admin_menu = True
                show_appointment_menu = False
                show_employee_menu = False 
                
            elif rid == 2:
                show_admin_menu = False
                show_appointment_menu = False
                show_employee_menu = True
                
            elif rid == 1:
                show_admin_menu = False
                show_appointment_menu = True 
                show_employee_menu = False
        
        self.admin_menu.menuAction().setVisible(show_admin_menu)
        self.appointment_menu.menuAction().setVisible(show_appointment_menu)
        self.employee_menu.menuAction().setVisible(show_employee_menu)
        self.file_menu.menuAction().setVisible(is_logged_in)

    def handle_logout(self):
        self.current_user = None
        self.update_ui_for_role(None)
        QMessageBox.information(self, "Bilgi", "Çıkış yapıldı.")

    def update_ui_for_role(self, user):
        if user:
            try:
                role = user.role.role_name
                msg = f"Hoşgeldiniz, {user.first_name} {user.last_name}"
                
                self.title_label.setText(msg)
                self.status_label.setText(f"Yetki: {role}")
                self.logo_label.setText("✨👤")
                self.buttons_widget.setVisible(False)
                self.update_menu_visibility(True)
                
                if hasattr(self, 'appointment_page'):
                    self.stacked_widget.removeWidget(self.appointment_page)
                    try:
                        self.appointment_page = AppointmentWindow(user, self)
                        self.stacked_widget.insertWidget(4, self.appointment_page)
                    except TypeError:
                        print("HATA: AppointmentWindow güncellenemedi.")
            except Exception as e:
                print(f"Arayüz güncelleme hatası: {e}")
        else:
            self.title_label.setText("Güzellik & Bakım Merkezi")
            self.status_label.setText("Devam etmek için lütfen giriş yapınız.")
            self.logo_label.setText("✂️💈")
            self.buttons_widget.setVisible(True)
            
            self.update_menu_visibility(False)
            self.stacked_widget.setCurrentIndex(0)

    def show_salon_management(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_employee_management(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_user_management(self):
        self.stacked_widget.setCurrentIndex(3)

    def show_appointment_window(self):
        self.stacked_widget.setCurrentIndex(4)

    def show_employee_dashboard(self):
        try:
            from ui.employee_dashboard import EmployeeDashboard
            self.emp_dashboard = EmployeeDashboard(self.current_user)
            self.emp_dashboard.show()
        except ImportError as ie:
            print(f"Panel Import Hatası: {ie}")
            QMessageBox.critical(self, "Hata", f"Personel paneli dosyası yüklenemedi:\n{ie}")
        except Exception as e:
            print(f"Panel Açılma Hatası: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Hata", f"Panel açılırken hata oluştu:\n{e}")

def exception_hook(exctype, value, tb):
    print("\n!!! BEKLENMEYEN ÇÖKME (CRASH) !!!")
    print("Hata:", value)
    traceback.print_exception(exctype, value, tb)
    sys.exit(1)

if __name__ == "__main__":
    sys.excepthook = exception_hook
    try:
        app = QApplication(sys.argv)
        if MODERN_THEME:
            app.setStyleSheet(MODERN_THEME)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"\n!!! BAŞLATMA HATASI: {e}")
        traceback.print_exc()