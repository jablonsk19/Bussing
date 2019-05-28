
pyinstaller.exe --paths C:\Python36\Lib\site-packages\PyQt5\Qt\bin --icon="HTA Logo.ico" --windowed --onedir --noconfirm --hidden-import PyQt5.sip hta.py 

copy main.qml dist\hta
copy "HTA Logo.png" dist\hta
copy "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64\*.dll" dist\hta

