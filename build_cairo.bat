call custom-dir.bat

python .\build_rdkit_csharp.py --build_freetype --build_platform all
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_platform all
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_libpng --build_platform all
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_pixman --build_platform all
if errorlevel 1 goto :ERROREND
python .\build_rdkit_csharp.py --build_cairo --build_platform all
if errorlevel 1 goto :ERROREND

goto :END

:ERROREND
exit /b 1

:END
