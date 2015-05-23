@echo off

del /F /Q win32
python build_win32.py py2exe -d win32
copy ..\tld.csv win32
copy ..\config.ini win32
