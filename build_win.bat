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

nmake -f Makefile.win rdkit_native PLATFORM=x86
@if errorlevel 1 goto :ERROREND
nmake -f Makefile.win rdkit_native PLATFORM=x64
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
