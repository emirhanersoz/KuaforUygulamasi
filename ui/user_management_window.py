from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QHeaderView, 
    QTableWidgetItem, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from database.db_connection import SessionLocal
from services.user_service import get_all_users, delete_user, update_user_role

class UserManagementWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kullanıcı Kontrol Merkezi")
        
        layout = QVBoxLayout()
        
        top_layout = QHBoxLayout()
        title = QLabel("Tüm Kullanıcılar (Admin Paneli)")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        refresh_btn = QPushButton("Listeyi Yenile")
        refresh_btn.clicked.connect(self.load_users)
        
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(refresh_btn)
        layout.addLayout(top_layout)

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "E-posta", "Rol", "Rol Değiştir", "İşlem"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.user_table)

        self.setLayout(layout)

    def load_users(self):
        self.user_table.setRowCount(0)
        try:
            with SessionLocal() as db:
                users = get_all_users(db)
                self.user_table.setRowCount(len(users))
                
                for row, user in enumerate(users):
                    role_name = user.role.role_name if user.role else "Yok"
                    
                    self.user_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
                    self.user_table.setItem(row, 1, QTableWidgetItem(f"{user.first_name} {user.last_name}"))
                    self.user_table.setItem(row, 2, QTableWidgetItem(user.email))
                    self.user_table.setItem(row, 3, QTableWidgetItem(role_name))
                    
                    combo = QComboBox()
                    combo.addItems(["Müşteri", "Çalışan", "Yönetici"])
                    combo.setCurrentText(role_name)

                    combo.currentTextChanged.connect(lambda text, uid=user.id: self.change_role(uid, text))
                    self.user_table.setCellWidget(row, 4, combo)

                    del_btn = QPushButton("Sil")
                    del_btn.setStyleSheet("background-color: #f44336; color: white;")
                    del_btn.clicked.connect(lambda checked, uid=user.id: self.delete_user_click(uid))
                    self.user_table.setCellWidget(row, 5, del_btn)
                    
        except Exception as e:
            print(f"Kullanıcı listesi hatası: {e}")

    def change_role(self, user_id, new_role):
        reply = QMessageBox.question(self, "Onay", f"Kullanıcı rolünü '{new_role}' olarak değiştirmek istiyor musunuz?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with SessionLocal() as db:
                    if update_user_role(db, user_id, new_role):
                        QMessageBox.information(self, "Başarılı", "Rol güncellendi.")
                        self.load_users()
                    else:
                        QMessageBox.warning(self, "Hata", "Rol güncellenemedi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", str(e))
        else:
            self.load_users() 

    def delete_user_click(self, user_id):
        reply = QMessageBox.question(self, "Silme Onayı", "Bu kullanıcıyı silmek istediğinize emin misiniz?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with SessionLocal() as db:
                    if delete_user(db, user_id):
                        self.load_users()
                        QMessageBox.information(self, "Başarılı", "Kullanıcı silindi.")
                    else:
                        QMessageBox.warning(self, "Hata", "Kullanıcı bulunamadı.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", str(e))