import sys
import cv2
import yaml
import re
import pyautogui
import pygetwindow as gw
from pyzbar.pyzbar import decode
from simpleaudio import sa
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer

class BarcodeScannerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.config = self.load_config()
        self.cap = None
        self.running = False
        self.last_barcode = None

        self.init_ui()

    def load_config(self):
        with open("config.yaml", "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def init_ui(self):
        self.setWindowTitle("Barcode Scanner")
        self.setGeometry(100, 100, 640, 480)

        self.video_label = QLabel(self)
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.toggle_scanning)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        self.timpythoner = QTimer()
        self.timer.timeout.connect(self.capture_frame)

    def toggle_scanning(self):
        if self.running:
            self.running = False
            self.start_button.setText("Start")
            self.timer.stop()
            if self.cap:
                self.cap.release()
        else:
            self.running = True
            self.start_button.setText("Stop")
            self.start_camera()
            self.timer.start(30)

    def start_camera(self):
        available_cameras = self.find_cameras()
        if not available_cameras:
            self.video_label.setText("No suitable cameras found.")
            return

        cam_id = self.config.get("camera_id", available_cameras[0])
        if cam_id not in available_cameras:
            cam_id = available_cameras[0]

        self.cap = cv2.VideoCapture(cam_id)

    def find_cameras(self):
        available_cameras = []
        for cam_id in range(5):
            cap = cv2.VideoCapture(cam_id)
            if cap.isOpened():
                available_cameras.append(cam_id)
                cap.release()
        return available_cameras

    def capture_frame(self):
        if not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        barcode = self.scan_barcode(frame)
        if barcode and barcode != self.last_barcode:
            self.last_barcode = barcode
            play_sound(self.config["sound"]["success"])
            self.process_barcode(barcode)

        elif barcode is None and self.last_barcode is not None:
            play_sound(self.config["sound"]["lost"])
            self.last_barcode = None

        self.display_frame(frame)

    def scan_barcode(self, frame):
        barcodes = decode(frame)
        for barcode in barcodes:
            return barcode.data.decode("utf-8")
        return None

    def process_barcode(self, barcode):
        parsed_data = self.parse_barcode(barcode, self.config["regex"])
        if parsed_data:
            window = self.find_window(self.config["window_title"])
            if window:
                x, y = self.config["input_position"]
                pyautogui.click(x, y)
                pyautogui.hotkey("ctrl", "a")
                pyautogui.press("backspace")
                pyautogui.write(parsed_data)

    def parse_barcode(self, barcode, regex):
        match = re.search(regex, barcode)
        return match.group("numericPart") if match else None

    def play_sound(sound_file):
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        wave_obj.play()

    def find_window(self, target):
        for window in gw.getWindowsWithTitle(target):
            if target.lower() in window.title.lower():
                return window
        return None

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        qimg = QImage(frame.data, width, height, width * 3, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarcodeScannerApp()
    window.show()
    sys.exit(app.exec())
