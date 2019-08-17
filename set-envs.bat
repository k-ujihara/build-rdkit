REM Customize 'custom-dir.bat'.
REM Before calling this batch,
REM 'SET BUILDPLATFORM=x86' when you build 32-bit platform,
REM 'SET BUILDPLATFORM=x64' when you build 32-bit platform.
REM If it is not specified, BUILDPLATFORM is set accrding to PROCESSOR_ARCHITECTURE value.

SET THISDIR=%~dp0
SET FORMER_BUILDPLATFORM=%BUILDPLATFORM%
IF "%BUILDPLATFORM%" == "" (
	IF "%PROCESSOR_ARCHITECTURE%" EQU "AMD64" SET BUILDPLATFORM=x64
	IF "%PROCESSOR_ARCHITECTURE%" EQU "x86"   SET BUILDPLATFORM=x86
)
SET BUILDPLATFORM_CHANGED=
IF "%FORCEADDPYTHONPATH%" NEQ "%BUILDPLATFORM%" SET BUILDPLATFORM_CHANGED=TRUE 

CALL "%THISDIR%custom-dir.bat"

IF "%BUILDPLATFORM%" == "x64" (
	SET CMAKEG=Visual Studio 15 2017 Win64
	SET MSBUILDPLATFORM=x64
	SET ADDRESSMODEL=64
) ELSE IF "%BUILDPLATFORM%" == "x86" (
	SET CMAKEG=Visual Studio 15 2017
	SET MSBUILDPLATFORM=Win32
	SET ADDRESSMODEL=32
) ELSE (
	ECHO Error: Unknown platform "%BUILDPLATFORM%".
	EXIT
)

SET BUILDDIR=build%BUILDPLATFORM%
SET BUILDDIRCSHARP=%BUILDDIR%CSharp

IF "%PYTHONDIR%" EQU "" (
	ECHO Error: PYTHONDIR is not specified.
	EXIT
) 

IF "%BUILDPLATFORM_CHANGED%" EQU "" GOTO L__ForceAddPythonPath
	PATH %PYTHONDIR%;%Path%
:L__PythonPathAdded

PUSHD %PYTHONDIR%
.\Scripts\pip install numpy

REM The followings are required to run tests.

REM To Path variable add Boost directory.
IF "%__BoostPathAdded%" NEQ "" GOTO L__BoostPathAdded
	PATH %BOOSTDIR%\stage\%BUILDPLATFORM%\lib;%Path%
	SET __BoostPathAdded=1
:L__BoostPathAdded

REM Envirnmental variable used by RDKit.
SET RDBASE=%RDKITDIR%

REM Add RDKit directory to PYTHONPATH to run with Python.
IF "%__RdkitDir_PythonPath_Added%" NEQ "" GOTO L__RdkitDir_PythonPath_Added
	SET PYTHONPATH=%RDKITDIR%;%PYTHONPATH%
	SET __RdkitDir_PythonPath_Added=1
:L__RdkitDir_PythonPath_Added

REM Some tests requires pandas and pillow package.
.\Scripts\pip install pandas
.\Scripts\pip install pillow
POPD

:END
