@echo off

call custom-dir.bat

python .\build_rdkit_csharp.py --build_freetype --build_platform all
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_zlib --build_platform all
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_libpng --build_platform all
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_pixman --build_platform all
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_cairo --build_platform all
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_rdkit --build_platform all
if errorlevel 1 goto :ERROREND
@rem wsl sudo hwclock -s
wsl bash build_rdkit.sh
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_wrapper
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_nuget
if errorlevel 1 goto :ERROREND

goto :END

:ERROREND
exit /b 1

:END
