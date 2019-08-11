# Build RDKit using Visual Studio 2017

This is to build RDKit for Windows with Visual Studio 2017. This is tested using the following versions.
- rdkit-Release_2019_03_3
- Boost 1.70.0
- Eigen 3.3.7
- zlib 1.2.11
- Python 3.6.8

## How to Build

- Install Visual Studio 2017.
- Install Python using installer enabling pip.
- Download and extract source codes of RDKit, Boost, zlib and Eigen3 to this directory.
- Customize 'set-envs.bat' file. 
- Open 'Developer Command Prompt for VS 2017'.
- ('SET BUILDPLATFORM=x86' for 32-bit, but it falls into SEGFAULT.)
- Execute 'build-all.bat'.
