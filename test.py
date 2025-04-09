import subprocess
import time
import signal

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
            print("☠️ LiveView ukončen.")
    else:
        print("ℹ️ LiveView byl ukončen.")

def take_photo(filename="photo.jpg", iso="1", aperture="9", shutter="1"):
    try:
        # subprocess.run(["gphoto2", "--set-config", "autofocus=0"])
        # time.sleep(1)  # počkej na zaostření
        subprocess.run(["gphoto2", "--set-config", f"iso={iso}"])
        subprocess.run(["gphoto2", "--set-config", f"aperture={aperture}"])
        subprocess.run(["gphoto2", "--capture-image-and-download", "--filename", "output/" + filename])
        print("📸 Fotka pořízena.")
    except subprocess.CalledProcessError as e:
        print("❌ Chyba při focení:", e)

def main_loop():
    while True:
        live_proc = None
        try:
            live_proc = start_liveview()
            time.sleep(5)  # necháme LiveView běžet 5 vteřin

            stop_liveview(live_proc)
            take_photo()

        except KeyboardInterrupt:
            print("🛑 Ukončeno uživatelem.")
            break
        finally:
            if live_proc:
                stop_liveview(live_proc)

if __name__ == "__main__":
    main_loop()
