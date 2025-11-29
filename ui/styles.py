MODERN_THEME = """
/* --- ANA PENCERE ARKA PLANI --- */
QMainWindow, QDialog {
    /* Soldan sağa: Çok açık pembe -> Çok açık mor */
    background-color: #fce4ec; /* Yüklenemezse bu renk olsun */
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fce4ec, stop:1 #f3e5f5);
}
QWidget {
    /* background: transparent;  <-- BU SATIRI SİLDİK, SİYAH YAPIYORDU */
    color: #4a148c; /* Yazılar: Koyu Mor */
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}
QGroupBox {
    background-color: rgba(255, 255, 255, 0.7);
    border: 1px solid #e1bee7;
    border-radius: 15px;
    margin-top: 25px;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 20px;
    padding: 5px 10px;
    color: #8e24aa; 
    background-color: #ffffff;
    border: 1px solid #e1bee7;
    border-radius: 10px;
}
QPushButton {
    background-color: #ffffff;
    color: #8e24aa;
    border: 1px solid #ce93d8;
    border-radius: 15px;
    padding: 8px 20px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #f3e5f5;
}
QPushButton:pressed {
    background-color: #e1bee7;
}
QPushButton[text="Onayla"], 
QPushButton[text="Giriş Yap"], 
QPushButton[text="Kayıt Ol"], 
QPushButton[text="Personel Ekle"],
QPushButton[text="Randevuyu Onayla"],
QPushButton[text="Saati Kaydet"],
QPushButton[text="Hizmeti Ekle / Güncelle"],
QPushButton[text="Listeyi Yenile"],
QPushButton[text="Listeyi Getir / Yenile"],
QPushButton[text="Verileri Getir / Yenile"],
QPushButton[text="Uygun Saatleri Göster"] {
    /* Soldan sağa: Pembe -> Mor Geçişi */
    background-color: #ec407a;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ec407a, stop:1 #ab47bc);
    color: white;
    border: none;
}
QPushButton[text="Onayla"]:hover, QPushButton[text="Giriş Yap"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d81b60, stop:1 #8e24aa);
}
QPushButton[text="Sil"], QPushButton[text="Reddet"], QPushButton[text="İptal"], QPushButton[text="Çıkış"] {
    border: 1px solid #ef9a9a;
    color: #e57373;
    background-color: #ffffff;
}
QPushButton[text="Sil"]:hover {
    background-color: #ffebee;
}
QLineEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #ce93d8;
    border-radius: 8px;
    padding: 6px;
    color: #4a148c;
    selection-background-color: #f8bbd0;
}
QLineEdit:focus, QComboBox:focus {
    border: 2px solid #ab47bc;
}
QMenuBar {
    background-color: #ffffff;
    color: #6a1b9a;
    border-bottom: 1px solid #e1bee7;
}
QMenuBar::item:selected {
    background-color: #f3e5f5;
    color: #ec407a;
}
QMenu {
    background-color: #ffffff;
    border: 1px solid #e1bee7;
    color: #4a148c;
}
QMenu::item:selected {
    background-color: #fce4ec;
    color: #ec407a;
}
QTableWidget {
    background-color: #ffffff;
    gridline-color: #f3e5f5;
    color: #4a148c;
    border: 1px solid #e1bee7;
}
QHeaderView::section {
    background-color: #f3e5f5;
    color: #6a1b9a;
    padding: 5px;
    border: none;
    border-bottom: 2px solid #ce93d8;
    font-weight: bold;
}
QStatusBar {
    background-color: #f3e5f5;
    color: #880e4f;
}
"""