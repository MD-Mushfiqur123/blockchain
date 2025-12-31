@echo off
echo Starting Advanced Blockchain GUI...
echo.
echo Choose GUI version:
echo 1. Simple GUI (no matplotlib) - Recommended
echo 2. Full GUI (with charts)
echo.
set /p choice="Enter choice (1 or 2): "
if "%choice%"=="1" (
    python run_simple_gui.py
) else if "%choice%"=="2" (
    python run_gui.py
) else (
    echo Using simple GUI by default...
    python run_simple_gui.py
)
pause

