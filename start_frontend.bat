@echo off

cd /d %~dp0

cd frontend

python -u -m http.server 5500