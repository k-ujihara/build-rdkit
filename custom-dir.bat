@rem Customize this file according to your environment.

@set THISDIR=%~dp0

set MINORVERSION=1
set RDKITDIR=%THISDIR%rdkit-Release_2020_09_3
set BOOSTDIR=%THISDIR%boost_1_74_0
set EIGENDIR=%THISDIR%eigen-3.3.8
set FREETYPEDIR=%THISDIR%freetype-2.10.4
set SWIG_DIR=%THISDIR%swigwin-4.0.2

@REM override MSVC option
set CL=/source-charset:utf-8 /execution-charset:utf-8

set SWIG_EXECUTABLE=%SWIG_DIR%\swig.exe
@where /Q swig
@if errorlevel 1 path %SWIG_DIR%;%Path%

:END
