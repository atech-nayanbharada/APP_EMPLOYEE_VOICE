@echo off

REM First project
set "original_dir=%CD%"
cd /d "D:\Projects\HR_SAMPARK"
call venv\hr_env\Scripts\activate
call cd project\HEC
start cmd /k "py manage.py runserver 0.0.0.0:7000"
cd /d "%original_dir%"



@echo off

REM First project
set "original_dir=%CD%"
cd /d "D:\Projects\Cricket"
call .venv\Scripts\activate
call cd AbexCricket_2
start cmd /k "py manage.py runserver 0.0.0.0:9000"
cd /d "%original_dir%"

