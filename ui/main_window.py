import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    """
    Uygulamanın ana penceresini temsil eder.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Kuaför/Berber Otomasyonu")
        self.setGeometry(100, 100, 800, 600) 

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.setup_ui()

    def setup_ui(self):
        """Arayüz bileşenlerini kurar."""

        title_label = QLabel("Kuaför/Berber Yönetim Sistemine Hoş Geldiniz")

        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        status_label = QLabel("Lütfen giriş yapın veya kayıt olun.")

        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet("font-size: 16px; color: #555;")

        self.layout.addWidget(title_label)
        self.layout.addWidget(status_label)

        self.create_menu_bar()

    def create_menu_bar(self):
        """Menü çubuğunu oluşturur."""
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Dosya")
        
        login_action = file_menu.addAction("Giriş Yap")
        exit_action = file_menu.addAction("Çıkış")
        exit_action.triggered.connect(self.close)
        
        help_menu = menu_bar.addMenu("Yardım")
        about_action = help_menu.addAction("Hakkında")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())