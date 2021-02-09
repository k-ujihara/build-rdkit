@where /Q python
@if errorlevel 1 goto :PYTHONERROR

@where /Q swig
@if errorlevel 1 goto :SWIGERROR

goto :GOEXEC

:PYTHONERROR
echo Python is not installed.
exit /b 1

:SWIGERROR
echo SWIG is not installed.
exit /b 1

:GOEXEC
@pushd %~dp0

@where /Q cl
@if errorlevel 1 goto :CL_NOT_FOUND

python .\build_rdkit_csharp.py --build_freetype --build_zlib --build_libpng --build_pixman --build_cairo --build_rdkit
@if errorlevel 1 goto :ERROREND

@rem wsl sudo hwclock -s
wsl python3 ./build_rdkit_csharp.py --build_rdkit
@if errorlevel 1 goto :ERROREND

python .\build_rdkit_csharp.py  --build_wrapper --build_nuget
@if errorlevel 1 goto :ERROREND

@goto :END

:ERROREND
@echo Something error happened.
goto :ERROREXIT

:CL_NOT_FOUND
@echo cl is not found. Execute 'Developer Command Prompt for VS 2019' first.
goto :ERROREXIT

:ERROREXIT
@popd
exit /b 1

:END
@popd
