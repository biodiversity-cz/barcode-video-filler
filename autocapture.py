import cv2
import yaml
import time
import re
import subprocess
import os
import signal
from pyzbar.pyzbar import decode
import pygame

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

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

def take_photo(filename="photo.jpg", iso="100", aperture="8", shutter="1"):
    subprocess.run(["gphoto2", "--set-config", "autofocus=1"])
    time.sleep(1)  # počkej na zaostření
    subprocess.run(["gphoto2", "--set-config", f"iso={iso}"])
    subprocess.run(["gphoto2", "--set-config", f"aperture={aperture}"])
    subprocess.run(["gphoto2", "--set-config", f"shutterspeed={shutter}"])
    subprocess.run(["gphoto2", "--capture-image-and-download", "--filename", filename])

class LiveViewController:
    def __init__(self, device="/dev/video10"):
        self.device = device
        self.process = None

    def start(self):
        if self.process is None or self.process.poll() is not None:
            cmd = (
                "gphoto2 --stdout --capture-movie | "
                f"stdbuf -oL ffmpeg -f mjpeg -i - "
                f"-vcodec rawvideo -pix_fmt yuv420p -f v4l2 {self.device}"
            )
            self.process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
            time.sleep(3)
            print("LiveView started.")

    def stop(self):
        if self.process and self.process.poll() is None:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process.wait()
            print("LiveView stopped.")
            time.sleep(2)

    def restart(self):
        self.stop()
        self.start()

def process_barcode(barcode, config, liveview):
    numeric_part = parse_barcode(barcode, config["regex"])
    if numeric_part:
        filename = f"{numeric_part}.jpg"
        play_sound(config["sound"]["success"])
        liveview.stop()
        take_photo(filename)
        liveview.start()


def main():
    config = load_config()
    pygame.mixer.init()

    cam_id = config.get("camera_id", "/dev/video10")

    cap = cv2.VideoCapture(cam_id)
    last_barcode = None
    liveview = LiveViewController()
    liveview.start()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame. Retrying...")
                continue

            barcode = scan_barcode(frame)
            if barcode and barcode != last_barcode:
                last_barcode = barcode
                print(f"New barcode detected: {barcode}")
                process_barcode(barcode, config, liveview)
            elif barcode is None and last_barcode is not None:
                print("Barcode lost.")
                play_sound(config["sound"]["lost"])
                last_barcode = None

            time.sleep(0.2)
        finally:
            liveview.stop()
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
