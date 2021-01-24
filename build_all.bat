call custom-dir.bat
@where /Q cl
@if errorlevel 1 goto :CL_NOT_FOUND

python .\build_rdkit_csharp.py --build_freetype --build_zlib --build_libpng --build_pixman --build_cairo --build_rdkit
@if errorlevel 1 goto :ERROREND

@rem wsl sudo hwclock -s
wsl bash build_rdkit.sh
@if errorlevel 1 goto :ERROREND

python .\build_rdkit_csharp.py  --build_wrapper --build_nuget --build_platform all
@if errorlevel 1 goto :ERROREND

@goto :END

:ERROREND
@echo Something error happened.
exit /b 1

:CL_NOT_FOUND
@echo cl is not found. Execute 'Developer Command Prompt for VS 2017' first.
exit /b 1

:END
