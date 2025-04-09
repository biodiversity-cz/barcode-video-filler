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

def start_liveview():
    cmd = [
        "bash", "-c",
        "gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -f v4l2 /dev/video10"
    ]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN)
    )
    print(f"▶️ LiveView PID: {proc.pid}")
    return proc

def stop_liveview(proc):
    if proc.poll() is None:
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=5)
            print("✅ LiveView úspěšně ukončen.")
        except subprocess.TimeoutExpired:
#             print("⚠️ Nešlo ukončit, zabíjím proces...")
            proc.kill()
            proc.wait()
            subprocess.run(["killall", "gphoto2"]) # i když znám id procesu tak to stejně nestačí, musím natvrdo
            print("☠️ LiveView ukončen.")
    else:
        print("ℹ️ LiveView byl ukončen.")

def take_photo(filename="photo.jpg", iso="1", aperture="15", shutter="1"):
    try:
        # subprocess.run(["gphoto2", "--set-config", "autofocus=0"])
        # time.sleep(1)  # počkej na zaostření
        subprocess.run(["gphoto2", "--set-config", f"iso={iso}"])
        subprocess.run(["gphoto2", "--set-config", f"aperture={aperture}"])
        subprocess.run(["gphoto2", "--capture-image-and-download", "--filename", "output/" + filename])
        print("📸 Fotka pořízena.")
    except subprocess.CalledProcessError as e:
        print("❌ Chyba při focení:", e)



def main():
    config = load_config()
    pygame.mixer.init()

    cam_id = config.get("camera_id", "/dev/video10")
    last_barcode = None
    live_proc = None
    cap = None

    while True:
        live_proc = None
        try:
            live_proc = start_liveview()
            time.sleep(3)
            cap = cv2.VideoCapture(cam_id, cv2.CAP_V4L2)
            if not cap.isOpened():
                print("Error opening video")
            print("CV started")
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to grab frame. Retrying...")
                    continue

                barcode = scan_barcode(frame)
                if barcode and barcode != last_barcode:
                    last_barcode = barcode
                    print(f"New barcode detected: {barcode}")
                    numeric_part = parse_barcode(barcode, config["regex"])
                    if numeric_part:
                        filename = f"PRC-{numeric_part}.jpg"
                        print(f"Let's capture photo with filename: {filename}")
                        play_sound(config["sound"]["success"])
                        break;
                    else:
                        play_sound(config["sound"]["wrong"])
            cap.release()
            stop_liveview(live_proc)
            time.sleep(1)
            take_photo(filename)
        except KeyboardInterrupt:
             print("🛑 Ukončeno uživatelem.")
             break
        finally:
            if cap:
                cap.release()
            if live_proc:
                stop_liveview(live_proc)

if __name__ == "__main__":
    main()
