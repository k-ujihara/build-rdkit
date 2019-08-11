IF "%__PythonPath_Added%" NEQ "" GOTO L__PythonPath_Added
	SET PYTHONPATH=%RDKITDIR%;%PYTHONPATH%
	SET __PythonPath_Added=1
:L__PythonPath_Added

IF "%__BoostPathAdded%" NEQ "" GOTO L__BoostPathAdded
	PATH %BOOSTDIR%\stage\%BUILDPLATFORM%\lib;%Path%
	SET __BoostPathAdded=1
:L__BoostPathAdded

SET RDBASE=%RDKITDIR%

PUSHD %RDKITDIR%
CD %BUILDDIR%
MSBuild RUN_TESTS.vcxproj /p:Configuration=Release,Platform=%MSBUILDPLATFORM% -maxcpucount:%NUMBER_OF_PROCESSORS%
POPD
