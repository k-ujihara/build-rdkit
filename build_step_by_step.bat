@echo off

call custom-dir.bat

python .\build-rdkit-csharp.py --build_freetype --build_platform all
if errorlevel 1 goto :END
python .\build-rdkit-csharp.py --build_rdkit --build_platform all
if errorlevel 1 goto :END
python .\build-rdkit-csharp.py --build_wrapper
if errorlevel 1 goto :END
python .\build-rdkit-csharp.py --build_nuget
if errorlevel 1 goto :END

:END
