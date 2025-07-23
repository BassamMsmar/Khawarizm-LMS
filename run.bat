@echo off
cd /d "D:\Projects-Django\College\venv\Khawarizm-LMS"

REM تفعيل البيئة الافتراضية داخل النافذة الجديدة وتشغيل السيرفر
start cmd /k "call ..\Scripts\activate && py manage.py runserver"

REM انتظار 3 ثواني لبدء السيرفر
timeout /t 3 >nul

REM فتح المتصفح
start http://127.0.0.1:8000
