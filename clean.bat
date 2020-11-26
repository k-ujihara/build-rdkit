@echo off
rem Erase all environmental variable used.

call :DELFILE "%RDKITDIR%\Code\JavaWrappers\csharp_wrapper\RDKit.DotNetWrap.nuspec"
call :DELFILE "%RDKITDIR%\Code\JavaWrappers\csharp_wrapper\RDKit.DotNetWrap.targets"
call :DELDIR "%RDKITDIR%\lib"
call :GODEL x64
call :DELDIR "%FREETYPEDIR%\objs\x64"
call :GODEL x86
call :DELDIR "%FREETYPEDIR%\objs\Win32"
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
call :DELDIR "%RDKITDIR%\Code\JavaWrappers\csharp_wrapper\%~1"
@rem The following directory is now used in building rdkit.
call :DELDIR "%THISDIR%build%~1CSharp"
@rem The following two are legacies.
call :DELDIR "%RDKITDIR%\build%~1"
call :DELDIR "%RDKITDIR%\build%~1CSharp
call :DELDIR "%ZLIBDIR%\build%~1"
exit /b

:DELDIR
if exist "%~1\" (
	rmdir /S /Q "%~1"
	echo "%~1" directory is removed.
)
exit/b

:DELFILE
if exist "%~1" (
	del /Q "%~1"
)
exit/b

:END
