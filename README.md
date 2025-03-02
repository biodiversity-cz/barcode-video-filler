# barcode-video-filler

## Configuration
Sound bank like https://pixabay.com/cs/sound-effects and search for "success" and "error" e.g.

## Build
### Ubuntu
I've started with pygetwindow, but this supports only Windows windows. At this moment no Ubuntu build available

```shell
sudo apt install -y python3 python3-pip libzbar0 build-essential python3-dev libasound2-dev python3-tk python3-pyqt6

python3.12 -m venv myenv
source myenv/bin/activate

pyinstaller --onefile --hidden-import=pyzbar.pyzbar --hidden-import=PIL --collect-binaries pyzbar barcod.py

deactivate
```
for debugging:
```shell
python3.12 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
xhost +local:

python3 barcode.py

deactivate
```

```shell
Add-Type -AssemblyName System.Windows.Forms
while (1) {
    $X = [System.Windows.Forms.Cursor]::Position.X
    $Y = [System.Windows.Forms.Cursor]::Position.Y

    Write-Host -NoNewline ("`rX:{0,6:D} | Y:{1,6:D}" -f $X,$Y)
}
```