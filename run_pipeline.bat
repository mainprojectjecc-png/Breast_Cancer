@echo off
REM ML Pipeline Runner Script
REM Runs the complete ML pipeline (CNN, SVM, QSVM, QVC)

cd /d "%~dp0"

echo Activating Python 3.11 virtual environment...
call .venv\Scripts\activate.bat

echo.
echo ============================================================
echo ML PIPELINE: CNN, SVM, QSVM, and QVC
echo ============================================================
echo.

python main.py

echo.
pause