
pyinstaller.exe --icon="HTA Logo.ico" --windowed --onedir --noconfirm --hidden-import PyQt5.sip hta.py 

copy main.qml dist\hta
copy "HTA Logo.png" dist\hta
