@echo off
title Flash NodeMCU (ESP8266) TX
echo ===================================================
echo   Flashing NodeMCU (ESP8266) Transmitter Firmware
echo ===================================================
echo.
python scripts\flash_board.py nodemcu_tx
if errorlevel 1 pause
