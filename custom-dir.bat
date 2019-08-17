REM Customize this file according to your environment.

SET RDKITDIR=%~dp0rdkit-Release_2019_03_3
SET BOOSTDIR=%~dp0boost_1_70_0
SET EIGENDIR=%~dp0eigen-eigen-323c052e1731
SET ZLIBDIR=%~dp0zlib-1.2.11
IF "%PYTHONDIR%" == "" (
	IF "%BUILDPLATFORM%" EQU "x64" SET PYTHONDIR=%LOCALAPPDATA%\Programs\Python\Python36
	IF "%BUILDPLATFORM%" EQU "x86" SET PYTHONDIR=%LOCALAPPDATA%\Programs\Python\Python36-32
)
