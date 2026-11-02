@echo off
title Flash ESP32 TX (Transmitter)
echo ===================================================
echo     Flashing ESP32 Transmitter (TX) Firmware
echo ===================================================
echo.
python scripts\flash_board.py tx
if errorlevel 1 pause
