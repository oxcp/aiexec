@echo off
setlocal enabledelayedexpansion

set "file=models.txt"
for /f "usebackq delims=" %%A in ("%file%") do (
    echo %%A
)

endlocal