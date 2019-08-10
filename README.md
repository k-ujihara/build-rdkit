# Build RDKit using Visual Studio 2017

This is to build RDKit for Windows with Visual Studio 2017. This is tested with rdkit-Release_2019_03_3, Boost 1.70.0, Eigen 3.3.7 and zlib 1.2.11.

## How to Build

- Download and extract source codes of RDKit, Boost, zlib and Eigen3 to this directory.
- Customize the some lines in 'build-all.bat'.

build-all.bat
```
REM Customize the following lines.

SET MODEL=64
SET RDKITDIR=%THISDIR%rdkit-Release_2019_03_3
SET BOOSTDIR=%THISDIR%boost_1_70_0
SET EIGENDIR=%THISDIR%eigen-eigen-323c052e1731
SET ZLIBDIR=%THISDIR%zlib-1.2.11
IF "%MODEL%" EQU "64" SET PYTHONDIR=C:\Python36
IF "%MODEL%" EQU "32" SET PYTHONDIR=C:\Python36

REM End Customize
```

- Open 'Developer Command Prompt for VS 2017'.
- Execute 'build-all.bat'.

