$ErrorActionPreference = "Stop"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --clean --windowed --name FocusFlow main.py
Write-Host "Build output: dist\FocusFlow\"
Write-Host "This is a development build. Test on a clean Windows machine."
