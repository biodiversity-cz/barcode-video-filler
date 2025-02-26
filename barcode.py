import cv2
import yaml
import time
import re
import pyautogui
import pygetwindow as gw
from pyzbar.pyzbar import decode

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def find_cameras():
    available_cameras = []
    for cam_id in range(10):  # Testuje prvních 10 kamerových ID
        cap = cv2.VideoCapture(cam_id)
        if cap.isOpened():
            available_cameras.append(cam_id)
            cap.release()
    return available_cameras

def scan_barcode(frame):
    barcodes = decode(frame)
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        return barcode_data
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

    screen_width, screen_height = pyautogui.size()
    print(f"Screen resolution: {screen_width}x{screen_height} (0,0 is top-left corner)")
    
    print(f"Available cameras: {available_cameras}")
    cam_id = config.get("camera_id", available_cameras[0])
    if cam_id not in available_cameras:
        print(f"Configured camera {cam_id} is not available, using {available_cameras[0]} instead.")
        cam_id = available_cameras[0]
    
    cap = cv2.VideoCapture(cam_id)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        barcode = scan_barcode(frame)
        if barcode:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"Barcode detected: {barcode} at {timestamp}")
            process_barcode(barcode, config)
        
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()

