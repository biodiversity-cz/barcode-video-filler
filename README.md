# barcode-video-filler

## Configuration
Visit sound bank like https://pixabay.com/cs/sound-effects and search for "success" and "error" e.g. Two sound file should be stored in the subfolder "./sound". The script expects also ./config.xaml in the current directory to set up configuration.

## Build
### Ubuntu
Using pygetwindow that supports only Windows windows. At this moment no Ubuntu build available.

### Windows
Only no_gui.py variant works.

```shell
pip install -r requirements.txt
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

[//]: # (obligatory branding for EOSC.CZ)
<hr style="margin-top: 100px; margin-bottom: 20px">

<p style="text-align: left"> <img src="https://webcentrum.muni.cz/media/3831863/seda_eosc.png" alt="EOSC CZ Logo" height="90"> </p>
This project output was developed with financial contributions from the EOSC CZ initiative throught the project National Repository Platform for Research Data (CZ.02.01.01/00/23_014/0008787) funded by Programme Johannes Amos Comenius (P JAC) of the Ministry of Education, Youth and Sports of the Czech Republic (MEYS).

<p style="text-align: left"> <img src="https://webcentrum.muni.cz/media/3832168/seda_eu-msmt_eng.png" alt="EU and MŠMT Logos" height="90"> </p>
