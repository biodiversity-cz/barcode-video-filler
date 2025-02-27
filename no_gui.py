import cv2
import yaml
import time
import re
import pyautogui
import pygetwindow as gw
from pyzbar.pyzbar import decode
from playsound import playsound

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def find_cameras():
    available_cameras = []
    for cam_id in range(5):
        cap = cv2.VideoCapture(cam_id)
        if cap.isOpened():
            available_cameras.append(cam_id)
            cap.release()
    return available_cameras

def scan_barcode(frame):
    barcodes = decode(frame)
    for barcode in barcodes:
        return barcode.data.decode("utf-8")
    return None

def parse_barcode(barcode, regex):
    match = re.search(regex, barcode)
    return match.group("numericPart") if match else None

def find_window(target):
    for window in gw.getWindowsWithTitle(target):
        if target.lower() in window.title.lower():
            return window
    return None

def process_barcode(barcode, config):
    parsed_data = parse_barcode(barcode, config["regex"])
    if parsed_data:
        window = find_window(config["window_title"])
        if window:
            x, y = config["input_position"]
            pyautogui.click(x, y)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("backspace")
            pyautogui.write(parsed_data)

def main():
    config = load_config()
    available_cameras = find_cameras()

    if not available_cameras:
        print("No suitable cameras found.")
        return

    cam_id = config.get("camera_id", available_cameras[0])
    if cam_id not in available_cameras:
        print(f"Configured camera {cam_id} is not available, using {available_cameras[0]} instead.")
        cam_id = available_cameras[0]

    cap = cv2.VideoCapture(cam_id)
    last_barcode = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        barcode = scan_barcode(frame)
        if barcode and barcode != last_barcode:
            last_barcode = barcode
            print(f"New barcode detected: {barcode}")
            playsound(config["sound"]["success"])
            process_barcode(barcode, config)
        elif barcode is None and last_barcode is not None:
            print("Barcode lost.")
            playsound(config["sound"]["lost"])
            last_barcode = None

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
