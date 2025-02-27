import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Nastavení okna
        self.setWindowTitle("Minimalistická GUI aplikace")
        self.setGeometry(100, 100, 300, 200)

        # Tlačítko
        self.button = QPushButton("Klikni mě", self)
        self.button.clicked.connect(self.on_click)
        self.button.resize(self.button.sizeHint())
        self.button.move(100, 70)

    def on_click(self):
        print("Tlačítko bylo kliknuto!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())
