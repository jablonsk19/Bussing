
pyinstaller.exe --icon="HTA Logo.ico" --windowed --onedir --noconfirm hta.py 

::copy main.qml dist\hta
copy "HTA Logo.png" dist\hta
copy "Gradient.png" dist\hta
::copy "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64\*.dll" dist\hta

