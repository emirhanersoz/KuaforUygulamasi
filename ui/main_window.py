import sys
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMessageBox, QStatusBar, QStackedWidget
)
from PyQt6.QtCore import Qt

try:
    from ui.login_window import LoginWindow
    from ui.register_window import RegisterWindow
    from ui.salon_management_window import SalonManagementWindow
    from ui.employee_management_window import EmployeeManagementWindow
    from ui.user_management_window import UserManagementWindow
    from ui.appointment_window import AppointmentWindow
    from ui.employee_dashboard import EmployeeDashboard
except Exception as e:
    print(f"Import Hatası: {e}")

class SafeUser:
    def __init__(self, data_dict):
        self.id = data_dict.get('id')
        self.first_name = data_dict.get('first_name')
        self.last_name = data_dict.get('last_name')
        self.email = data_dict.get('email')
        self.role = type('Role', (), {'role_name': data_dict.get('role_name')})()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kuaför/Berber Otomasyonu")
        self.setGeometry(100, 100, 1100, 750)
        
        self.current_user = None 
        self.stacked_widget = QStackedWidget() 
        self.setCentralWidget(self.stacked_widget)
        self.status_label = QLabel() 

        self.setup_ui()
        
        try:
            self.add_management_pages()
        except Exception as e:
            print(f"Sayfa yükleme hatası: {e}")

        self.update_ui_for_role(None) 
        self.statusBar().showMessage("Sistem Hazır.")

    def setup_ui(self):
        self.setStatusBar(QStatusBar(self)) 
        self.create_menu_bar()
        
        welcome_page = QWidget()
        welcome_layout = QVBoxLayout(welcome_page)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 20px; color: #333;")
        self.status_label.setText("Kuaför Otomasyonuna Hoşgeldiniz\nLütfen Dosya > Giriş Yap menüsünü kullanın.")
        welcome_layout.addWidget(self.status_label)
        self.stacked_widget.addWidget(welcome_page)

    def add_management_pages(self):
        self.salon_management_page = SalonManagementWindow(self)
        self.stacked_widget.addWidget(self.salon_management_page)

        self.employee_management_page = EmployeeManagementWindow(self)
        self.stacked_widget.addWidget(self.employee_management_page)

        self.user_management_page = UserManagementWindow(self)
        self.stacked_widget.addWidget(self.user_management_page)

        self.appointment_page = AppointmentWindow(self)
        self.stacked_widget.addWidget(self.appointment_page)
        
        self.page_indices = {
            "welcome": 0,
            "salon_management": 1,
            "employee_management": 2,
            "user_management": 3,
            "appointments": 4,
        }

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        self.file_menu = menu_bar.addMenu("Dosya")
        self.admin_menu = menu_bar.addMenu("Yönetim")
        self.appointment_menu = menu_bar.addMenu("Randevular")
        
        self.login_action = self.file_menu.addAction("Giriş Yap")
        
        self.register_action = self.file_menu.addAction("Kayıt Ol")
        
        self.logout_action = self.file_menu.addAction("Çıkış Yap")
        self.exit_action = self.file_menu.addAction("Çıkış")
        
        self.manage_salon_action = self.admin_menu.addAction("Salonları Yönet")
        self.manage_employees_action = self.admin_menu.addAction("Personel Yönet (Eski)")
        
        self.manage_users_action = self.admin_menu.addAction("Tüm Kullanıcıları Yönet")
        
        self.view_appointments_action = self.appointment_menu.addAction("Randevu Takvimi")

        self.login_action.triggered.connect(self.open_login_window)
        self.register_action.triggered.connect(self.open_register_window)
        self.logout_action.triggered.connect(self.handle_logout)
        self.exit_action.triggered.connect(self.close)
        
        self.manage_salon_action.triggered.connect(self.show_salon_management)
        self.manage_employees_action.triggered.connect(self.show_employee_management)
        self.manage_users_action.triggered.connect(self.show_user_management)
        self.view_appointments_action.triggered.connect(self.show_appointment_window)

        self.employee_menu = menu_bar.addMenu("Personel Paneli")
        self.open_emp_dashboard = self.employee_menu.addAction("Çalışma Masam")
        self.open_emp_dashboard.triggered.connect(self.show_employee_dashboard)

        self.update_menu_visibility(False)

    def open_login_window(self):
        try:
            login_dialog = LoginWindow(self)
            if login_dialog.exec():
                data_dict = login_dialog.user_data_dict
                if data_dict:
                    self.current_user = SafeUser(data_dict)
                    self.update_ui_for_role(self.current_user)
        except Exception as e:
            print(f"Login penceresi açılırken hata: {e}")

    def open_register_window(self):
        try:
            reg_dialog = RegisterWindow(self)
            reg_dialog.exec()
        except Exception as e:
            print(f"Kayıt penceresi hatası: {e}")

    def update_menu_visibility(self, is_logged_in: bool):
        self.login_action.setVisible(not is_logged_in)
        self.register_action.setVisible(not is_logged_in)
        self.logout_action.setVisible(is_logged_in)
        
        is_admin = False
        if is_logged_in and self.current_user:
            if self.current_user.role.role_name == "Yönetici":
                is_admin = True
        
        is_employee = False
        if is_logged_in and self.current_user:
            role = self.current_user.role.role_name
            if role in ["Çalışan", "Yönetici"]:
                is_employee = True
        
        self.admin_menu.menuAction().setVisible(is_admin)
        self.appointment_menu.menuAction().setVisible(is_logged_in)
        self.employee_menu.menuAction().setVisible(is_employee)

    def handle_logout(self):
        self.current_user = None
        self.update_ui_for_role(None)
        QMessageBox.information(self, "Bilgi", "Çıkış yapıldı.")

    def update_ui_for_role(self, user):
        if user:
            try:
                msg = f"Hoşgeldiniz, {user.first_name} {user.last_name}\nRol: {user.role.role_name}"
                self.status_label.setText(msg)
                self.update_menu_visibility(True)
            except Exception as e:
                print(f"Rol güncelleme hatası: {e}")
        else:
            self.status_label.setText("Lütfen giriş yapınız.")
            self.update_menu_visibility(False)
            self.stacked_widget.setCurrentIndex(0)

    def show_salon_management(self):
        self.stacked_widget.setCurrentIndex(self.page_indices["salon_management"])

    def show_employee_management(self):
        self.stacked_widget.setCurrentIndex(self.page_indices["employee_management"])

    def show_user_management(self):
        self.stacked_widget.setCurrentIndex(self.page_indices["user_management"])

    def show_appointment_window(self):
        self.stacked_widget.setCurrentIndex(self.page_indices["appointments"])

    def show_employee_dashboard(self):
        try:
            self.emp_dashboard = EmployeeDashboard(self.current_user)
            self.emp_dashboard.show()
        except Exception as e:
            print(f"Panel hatası: {e}")    
            
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"\n!!! KRİTİK HATA: {e}")
        input("Kapanmak için Enter'a bas...")