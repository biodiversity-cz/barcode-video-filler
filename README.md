# barcode-video-filler
The very first attempt was to create a robot that independently detect barcode, navigate in specific window and capture a photo via pygetwindow "click". This approach was left and now focusing on Linux based auto-capture script without proprietary sw that has to be handled and "GUI coordinates" dependencies.

**Stack:** Canon 600D + Ubuntu PC. Canon runs in LiveView, when barcode detected, beep and take a photo running as a loop.

## preliminary
Visit sound bank like https://pixabay.com/cs/sound-effects and search for "success", "wrong" and "error" e.g. Two sound file should be stored in the subfolder "./sound". The script expects also ./config.yaml in the current directory to set up configuration.

## configure Canon as a source of barcode as well as a capture device

```shell
#check cameras' list and setup in config.yaml
v4l2-ctl --list-devices
#play image from some..
ffplay /dev/video4
# to list controls of specific camera
v4l2-ctl -d /dev/video4 -l
```
1) Canon 600D does not support UVC(https://en.wikipedia.org/wiki/USB_video_device_class), we need more tools
```sudo apt install v4l2loopback-dkms gphoto2```

2) make virtual camera slot: ```sudo modprobe v4l2loopback video_nr=10 card_label="CanonDSLR" exclusive_caps=1``` (/dev/video10 is now available, yet empty)

3) run LiveView and stream via ffmpeg to virtual camera ```gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -f v4l2 /dev/video10```

very probably, this ends up with an error *Could not claim interface* - we need to "free" the device:

```shell
killall gvfs-gphoto2-volume-monitor
killall gnome-settings-daemon
killall shotwell
#for permanent make udev rule:
sudo nano /etc/udev/rules.d/90-libgphoto2.rules
#ATTRS{idVendor}=="04a9", ENV{ID_GPHOTO2}="0" # 04a9 is Canon vendor ID
```  

4) unplug&plugin Canon and check ```gphoto2 --auto-detect```

## Run

```shell
sudo apt install libzbar-dev
python3 -m venv scheda
source scheda/bin/activate

pip install -r requirements.txt

python autocapture.py
```





## pygetwindow
Pygetwindow works only on Windows, kept only for evidence (gui_old.py)


**script for PowerShell to detect exact coordinates on the screen**
```shell
Add-Type -AssemblyName System.Windows.Forms
while (1) {
    $X = [System.Windows.Forms.Cursor]::Position.X
    $Y = [System.Windows.Forms.Cursor]::Position.Y

    Write-Host -NoNewline ("`rX:{0,6:D} | Y:{1,6:D}" -f $X,$Y)
}
```