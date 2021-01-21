@REM Customize this file according to your environment.

@set THIS_DIR=%~dp0

set MINOR_VERSION=3
set RDKIT_DIR=%THIS_DIR%rdkit-Release_2020_09_3
set BOOST_DIR=%THIS_DIR%boost_1_74_0
set EIGEN_DIR=%THIS_DIR%eigen-3.3.8
set FREETYPE_DIR=%THIS_DIR%freetype-2.10.4
set CAIRO_DIR=%THIS_DIR%cairo-1.16.0
set ZLIB_DIR=%THIS_DIR%zlib-1.2.11
set LIBPNG_DIR=%THIS_DIR%lpng1637
set PIXMAN_DIR=%THIS_DIR%pixman-0.40.0
set SWIG_DIR=%THIS_DIR%swigwin-4.0.2

set SWIG_EXECUTABLE=%SWIG_DIR%\swig.exe
@where /Q swig
@if errorlevel 1 path %SWIG_DIR%;%Path%

:END
