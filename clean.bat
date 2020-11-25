@echo off
rem Erase all environmental variable used.

call :GODEL x64
call :GODEL x86
if exist "%RDKITDIR%\Code\JavaWrappers\csharp_wrapper\RDKit.DotNetWrap.nuspec" del /Q "%RDKITDIR%\Code\JavaWrappers\csharp_wrapper\RDKit.DotNetWrap.nuspec"
if exist "%RDKITDIR%\Code\JavaWrappers\csharp_wrapper\RDKit.DotNetWrap.targets" del /Q "%RDKITDIR%\Code\JavaWrappers\csharp_wrapper\RDKit.DotNetWrap.targets"
call :CLEARENVVARS

goto :END

:CLEARENVVARS
set $EXE=
set BOOSTDIR=
set ZLIBDIR=
set RDKITDIR=
set EIGENDIR=
set BUILDDIR=
set BUILDDIRCSHARP=
set BUILDPLATFORM=
set BUILDPLATFORM_CHANGED=
set CMAKEG=
set PYTHONDIR=
set RDBASE=
set ADDRESSMODEL=
set THISDIR=
set FORMER_BUILDPLATFORM=
set BUILDPLATFORM_CHANGED=
rem set __RdkitDir_PythonPath_Added=
exit /b

:GODEL
rem Delete built directory.
echo Clean platform %~1.
call custom-dir.bat
call :DEL1 "%RDKITDIR%\build%~1"
call :DEL1 "%RDKITDIR%\Code\JavaWrappers\csharp_wrapper\%~1"
call :DEL1 "%RDKITDIR%\build%~1CSharp
call :DEL1 "%ZLIBDIR%\build%~1"
exit /b

:DEL1
if exist "%~1\" (
	rmdir /S /Q "%~1"
	echo "%~1" directory is removed.
)
exit/b

:END
