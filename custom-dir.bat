@rem Customize this file according to your environment.

@rem To select Python, uncomment and customize next line.
@rem set PYTHONVERSION=Python36

@rem set RDKITDIR=%THISDIR%rdkit-Release_2019_03_3
set RDKITDIR=%THISDIR%rdkit-Release_2019_09_1
set BOOSTDIR=%THISDIR%boost_1_70_0
set EIGENDIR=%THISDIR%eigen-eigen-323c052e1731
set ZLIBDIR=%THISDIR%zlib-1.2.11
set SWIGDIR=%THISDIR%swigwin-4.0.1

@where swig
@if errorlevel 1 goto :ADDSWIGPATH
goto :END

:ADDSWIGPATH
path %SWIGDIR%;%Path%

:END
