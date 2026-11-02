@echo off
title Flash ESP32 RX (Receiver)
echo ===================================================
echo     Flashing ESP32 Receiver (RX) Firmware
echo ===================================================
echo.
python scripts\flash_board.py rx
if errorlevel 1 pause
