from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QHeaderView, 
    QTableWidgetItem, QHBoxLayout, QMessageBox, QComboBox, QGroupBox, QFormLayout, QLineEdit
)
from PyQt6.QtCore import Qt
from database.db_connection import SessionLocal
from services.user_service import get_all_users, delete_user, update_user_details

class UserManagementWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kullanıcı Kontrol Merkezi")
        self.current_user_id = None
        
        main_layout = QVBoxLayout()
        
        form_group = QGroupBox("Kullanıcı Bilgileri Düzenle")
        form_layout = QFormLayout()
        
        self.fname_input = QLineEdit()
        self.lname_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        
        form_layout.addRow("Ad:", self.fname_input)
        form_layout.addRow("Soyad:", self.lname_input)
        form_layout.addRow("E-posta:", self.email_input)
        form_layout.addRow("Telefon:", self.phone_input)
        
        btn_layout = QHBoxLayout()
        self.update_btn = QPushButton("Bilgileri Güncelle")
        self.update_btn.clicked.connect(self.handle_update)
        self.update_btn.setEnabled(False)
        
        self.clear_btn = QPushButton("Seçimi Kaldır")
        self.clear_btn.clicked.connect(self.clear_form)
        
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.clear_btn)
        form_layout.addRow(btn_layout)
        
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Kullanıcı Listesi:"))
        refresh_btn = QPushButton("Listeyi Yenile")
        refresh_btn.clicked.connect(self.load_users)
        top_layout.addWidget(refresh_btn)
        main_layout.addLayout(top_layout)

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["ID", "Ad", "Soyad", "E-posta", "Telefon", "Rol"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.user_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.user_table.itemClicked.connect(self.on_row_clicked)
        
        main_layout.addWidget(self.user_table)
        self.setLayout(main_layout)
        
        self.load_users()

    def load_users(self):
        self.user_table.setRowCount(0)
        try:
            with SessionLocal() as db:
                users = get_all_users(db)
                self.user_table.setRowCount(len(users))
                
                for row, user in enumerate(users):
                    role_name = user.role.role_name if user.role else "Yok"
                    
                    self.user_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
                    self.user_table.setItem(row, 1, QTableWidgetItem(user.first_name))
                    self.user_table.setItem(row, 2, QTableWidgetItem(user.last_name))
                    self.user_table.setItem(row, 3, QTableWidgetItem(user.email))
                    self.user_table.setItem(row, 4, QTableWidgetItem(user.phone_number or ""))
                    self.user_table.setItem(row, 5, QTableWidgetItem(role_name))
                    
        except Exception as e:
            print(f"Kullanıcı listesi hatası: {e}")

    def on_row_clicked(self, item):
        row = item.row()
        self.current_user_id = int(self.user_table.item(row, 0).text())
        
        self.fname_input.setText(self.user_table.item(row, 1).text())
        self.lname_input.setText(self.user_table.item(row, 2).text())
        self.email_input.setText(self.user_table.item(row, 3).text())
        self.phone_input.setText(self.user_table.item(row, 4).text())
        
        self.update_btn.setEnabled(True)
        self.update_btn.setText("Seçili Kullanıcıyı Güncelle")

    def clear_form(self):
        self.current_user_id = None
        self.fname_input.clear()
        self.lname_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.update_btn.setEnabled(False)
        self.update_btn.setText("Bilgileri Güncelle")
        self.user_table.clearSelection()

    def handle_update(self):
        if not self.current_user_id: return
        
        fname = self.fname_input.text()
        lname = self.lname_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        
        try:
            with SessionLocal() as db:
                if update_user_details(db, self.current_user_id, fname, lname, email, phone):
                    QMessageBox.information(self, "Başarılı", "Kullanıcı bilgileri güncellendi.")
                    self.load_users()
                    self.clear_form()
                else:
                    QMessageBox.warning(self, "Hata", "Güncelleme başarısız.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))