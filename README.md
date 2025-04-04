# barcode-video-filler

## Configuration
Visit sound bank like https://pixabay.com/cs/sound-effects and search for "success" and "error" e.g. Two sound file should be stored in the subfolder "./sound". The script expects also ./config.xaml in the current directory to set up configuration.

## Build
### Ubuntu
Using pygetwindow that supports only Windows windows. At this moment no Ubuntu build available.

### Windows
Only no_gui.py variant works.

```shell
sudo apt install libzbar-dev
python3 -m venv scheda
source scheda/bin/activate

pip install -r requirements.txt

#check camera ID
v4l2-ctl --list-devices
#nebo 
ffplay /dev/video4
# use integer from name like /dev/videoX
# setup in config.yaml

python no_gui.py
```

**script for PowerShell to detect exact coordinates on the screen**
```shell
Add-Type -AssemblyName System.Windows.Forms
while (1) {
    $X = [System.Windows.Forms.Cursor]::Position.X
    $Y = [System.Windows.Forms.Cursor]::Position.Y

    Write-Host -NoNewline ("`rX:{0,6:D} | Y:{1,6:D}" -f $X,$Y)
}
```