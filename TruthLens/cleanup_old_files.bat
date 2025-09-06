@echo off
echo ================================================
echo TruthLens - Cleanup Old Streamlit Files
echo ================================================
echo.
echo This will create a backup zip and remove old files
echo.

echo Creating backup zip file...
powershell -Command "Compress-Archive -Path 'app.py', 'config.py', 'requirements.txt', 'pages', 'utils', 'assets', 'deploy', 'README.md', 'ADMIN_ACCESS.md', '__pycache__' -DestinationPath 'TruthLens_Old_Streamlit_Backup.zip' -Force"

echo.
echo Backup created: TruthLens_Old_Streamlit_Backup.zip
echo.

set /p confirm="Are you sure you want to delete the old files? (y/n): "
if /i "%confirm%"=="y" (
    echo.
    echo Removing old files...
    del app.py
    del config.py
    del requirements.txt
    del README.md
    del ADMIN_ACCESS.md
    rmdir /s /q pages
    rmdir /s /q utils
    rmdir /s /q assets
    rmdir /s /q deploy
    rmdir /s /q __pycache__
    echo.
    echo Old files removed successfully!
    echo Backup is saved as: TruthLens_Old_Streamlit_Backup.zip
) else (
    echo.
    echo Cleanup cancelled. Old files remain.
)

echo.
echo ================================================
echo Cleanup complete!
echo ================================================
pause
