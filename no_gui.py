import cv2
import yaml
import time
import re
from pyzbar.pyzbar import decode 
import pygame

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
    match = re.search(regex, barcode, re.IGNORECASE)
    if match:
        print("matched ID: " + match.group("numericPart")) 
    else:
        print("No match on: " + barcode)
    return match.group("numericPart") if match else None

def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()

def process_barcode(barcode, config):
    numeric_part = parse_barcode(barcode, config["regex"])
    if numeric_part:
        timestamp = int(time.time())
        filename = config["filename_template"].format(numeric_part=numeric_part.zfill(config["digits"]), timestamp=timestamp)
        play_sound(config["sound"]["success"])	


def main():
    config = load_config()
    available_cameras = find_cameras()
    pygame.mixer.init()

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
            print("Failed to grab frame. Retrying...")
            continue

        barcode = scan_barcode(frame)
        if barcode and barcode != last_barcode:
            last_barcode = barcode
            print(f"New barcode detected: {barcode}")
            process_barcode(barcode, config)
        elif barcode is None and last_barcode is not None:
            print("Barcode lost.")
            play_sound(config["sound"]["lost"])
            last_barcode = None
			
        time.sleep(0.5)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
