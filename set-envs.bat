@rem Customize 'custom-dir.bat'.
@rem Before calling this batch,
@rem 'set BUILDPLATFORM=x86' when you build for 32-bit platform,
@rem 'set BUILDPLATFORM=x64' when you build for 64-bit platform.
@rem if not specified, BUILDPLATFORM is set accrding to PROCESSOR_ARCHITECTURE value.

@set THISDIR=%~dp0

@rem Datermine BUILDPLATFORM and set variables.
@set FORMER_BUILDPLATFORM=%BUILDPLATFORM%
@if "%BUILDPLATFORM%" == "" (
	if "%PROCESSOR_ARCHITECTURE%" EQU "AMD64" set BUILDPLATFORM=x64
	if "%PROCESSOR_ARCHITECTURE%" EQU "x86"   set BUILDPLATFORM=x86
)
@echo BUILDPLATFORM is "%BUILDPLATFORM%".
@set BUILDPLATFORM_CHANGED=
@if "%FORMER_BUILDPLATFORM%" NEQ "%BUILDPLATFORM%" set BUILDPLATFORM_CHANGED=TRUE 
@if "%BUILDPLATFORM_CHANGED%" NEQ "" if "%FORMER_BUILDPLATFORM%" NEQ "" (
	@echo Build plarform is changed from %FORMER_BUILDPLATFORM% to %BUILDPLATFORM%.
)
@if "%BUILDPLATFORM%" EQU "x64" (
	set CMAKEG=Visual Studio 15 2017 Win64
	set MSBUILDPLATFORM=x64
	set ADDRESSMODEL=64
) else if "%BUILDPLATFORM%" EQU "x86" (
	set CMAKEG=Visual Studio 15 2017
	set MSBUILDPLATFORM=Win32
	set ADDRESSMODEL=32
) else (
	echo Error: Unknown platform "%BUILDPLATFORM%".
	exit
)
@set BUILDDIR=build%BUILDPLATFORM%
@set BUILDDIRCSHARP=%BUILDDIR%CSharp
@echo CMAKEG=%CMAKEG%
@echo MSBUILDPLATFORM=%MSBUILDPLATFORM%
@echo ADDRESSMODEL=%ADDRESSMODEL%
@echo BUILDDIR=%BUILDDIR%
@echo BUILDDIRCSHARP=%BUILDDIRCSHARP%

@call "%THISDIR%custom-dir.bat"

@rem Setup Python info
@if "%PYTHONVERSION%" EQU "" (
	call :SELECTPYTHONVERSION Python36
	call :SELECTPYTHONVERSION Python37
	call :SELECTPYTHONVERSION Python38
)
@if "%PYTHONVERSION%" EQU "" (
	@echo Error: PYTHONVERSION could not be specified.
	@exit
)
@echo PYTHONVERSION=%PYTHONVERSION%
@if "%BUILDPLATFORM%" EQU "x64" if exist "%LOCALAPPDATA%\Programs\Python\%PYTHONVERSION%\"    set PYTHONDIR=%LOCALAPPDATA%\Programs\Python\%PYTHONVERSION%
@if "%BUILDPLATFORM%" EQU "x86" if exist "%LOCALAPPDATA%\Programs\Python\%PYTHONVERSION%-32\" set PYTHONDIR=%LOCALAPPDATA%\Programs\Python\%PYTHONVERSION%-32
@if "%PYTHONDIR%" EQU "" (
	@echo Error: PYTHONDIR is not specified.
	@exit
)
@goto :L__ENDSETUPPYTHONINFO
:SELECTPYTHONVERSION
@if "%BUILDPLATFORM%" EQU "x64" if exist "%LOCALAPPDATA%\Programs\Python\%~1\"    set PYTHONVERSION=%~1
@if "%BUILDPLATFORM%" EQU "x86" if exist "%LOCALAPPDATA%\Programs\Python\%~1-32\" set PYTHONVERSION=%~1
@exit /b
:L__ENDSETUPPYTHONINFO

@if "%BUILDPLATFORM_CHANGED%" NEQ "" goto :L__AddPythonDirToPATH
@echo "%Path%" | @find "%PYTHONDIR%">nul
@if not ERRORLEVEL 1 goto :L__EndPYTHONDIR
:L__AddPythonDirToPATH
	@echo Add %PYTHONDIR% to PATH.
	@PATH %PYTHONDIR%;%Path%
:L__EndPYTHONDIR

@pushd "%PYTHONDIR%"
@echo Install numpy.
@.\Scripts\pip install numpy

@rem The followings are required to run tests.

@rem To Path variable add Boost directory.
@if "%BUILDPLATFORM_CHANGED%" EQU "" goto :L__EndAddedBOOSTDIRtoPATH
	@echo Add %BOOSTDIR%\stage\%BUILDPLATFORM%\lib to PATH.
	@PATH %BOOSTDIR%\stage\%BUILDPLATFORM%\lib;%Path%
)
:L__EndAddedBOOSTDIRtoPATH

@rem Envirnmental variable used by RDKit.
@set RDBASE=%RDKITDIR%
@echo RDBASE=%RDBASE%

@rem Add RDKit directory to PYTHONPATH to run with Python.
@if "%PYTHONPATH%" EQU "" goto :L__RdkitDir_SetPYTHONPATH
@echo "%PYTHONPATH%" | find "%RDKITDIR%"
@if not ERRORLEVEL 1 goto :L__RdkitDir_PythonPath_Added
:L__RdkitDir_SetPYTHONPATH
@echo Add %RDKITDIR% to PYTHONPATH.
@set PYTHONPATH=%RDKITDIR%;%PYTHONPATH%
:L__RdkitDir_PythonPath_Added

@rem Some tests requires pandas and pillow package.
@echo Install pandas.
@.\Scripts\pip install pandas
@echo Install pillow.
@.\Scripts\pip install pillow
@popd

@goto :END

:END
