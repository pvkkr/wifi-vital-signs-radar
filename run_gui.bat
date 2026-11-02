@echo off
title WiFi Vital Signs Radar - CSI Live Monitor
echo ===================================================
echo   Starting WiFi Vital Signs Radar Dashboard...
echo ===================================================
python gui\live_monitor.py
if errorlevel 1 pause
