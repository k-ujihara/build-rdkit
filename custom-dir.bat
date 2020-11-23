@rem Customize this file according to your environment.

@rem To select Python, uncomment and customize next line.
@rem set PYTHONVERSION=Python36

set MINORVERSION=2

set RDKITDIR=%THISDIR%rdkit-Release_2019_09_1
set BOOSTDIR=%THISDIR%boost_1_74_0
set EIGENDIR=%THISDIR%eigen-3.3.8
set ZLIBDIR=%THISDIR%zlib-1.2.11
set FREETYPEDIR=%THISDIR%freetype-2.10.4
set SWIGDIR=%THISDIR%swigwin-4.0.2

@REM override MSVC option
set CL=/source-charset:utf-8 /execution-charset:utf-8

@where /Q swig
@if errorlevel 1 goto :ADDSWIGPATH
goto :END

:ADDSWIGPATH
path %SWIGDIR%;%Path%

:END
