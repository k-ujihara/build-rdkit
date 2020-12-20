# RDKit for .NET Framework

- .NET Framework wrapper of RDKit.
- NuGet package is available at [https://www.nuget.org/packages/RDKit.DotNetWrap/](https://www.nuget.org/packages/RDKit.DotNetWrap/).

- Example codes are in `RDKit2DotNet.Example` directory.

- Registered NuGet package was built using the following versions.
  - [RDKit Release_2020.09.3](https://github.com/rdkit/rdkit/releases/tag/Release_2020_09_3) and [RDKit Release_2019.09.1](https://github.com/rdkit/rdkit/releases/tag/Release_2019_09_1)
  - [Boost 1.74.0](https://sourceforge.net/projects/boost/files/boost-binaries/1.74.0/)
  - [Eigen 3.3.8](https://gitlab.com/libeigen/eigen/-/releases/3.3.8)
  - [Python](https://www.python.org/) 3.8.3
  - [CMAKE](https://cmake.org/) 3.12.18081601-MSVC_2
  - [SWIG](http://www.swig.org/) 4.0.2
  - [NuGet](https://nuget.org) 5.3.1
  - Visual Studio 2017

## How to Build

### Preparation

- Use Windows 10 (x64).
- Install Visual Studio 2017 enabling C++, C&#35; and CMAKE.
- Install Python into _default folder_ enabling pip using offical installer.
- Clone this repository to some directory. A short name is highly recommended for the directory.
- Download the following source archives and extract them here.
  - [RDKit](hhttps://github.com/rdkit/rdkit/) to `rdkit-Release_####_##_#`  
  - [Eigen3](http://eigen.tuxfamily.org/) to `eigen-#.#.#`
  - [SWIG](http://www.swig.org/) to `swigwin-#.#.#`
- Download binery archives of both 32-bit and 64-bit versions of Boost for Visual Studio 2017, ie, msvc-14.1.
  - [https://sourceforge.net/projects/boost/files/boost-binaries/](https://sourceforge.net/projects/boost/files/boost-binaries/).
  - Execute EXE files to extract. Defaults to store to `C:\local`.
  - Copy `boost_#_##_#` directory here.
  - Only dll and lib, ie, the files in `lib64-msvc-14.1` and `lib32-msvc-14.1`, are used to build.
  - After above, `lib64-msvc-14.1` and `lib32-msvc-14.1` should be created under `boost_#_##_#` directory.

- Customize `custom-dir.bat` file according to where above dependencies are installed.

### Build and create NuGet package

- Open 'Developer Command Prompt for VS 2017'.
- Execute `build_all.bat`.
  - Procedure to build them step by step is described below.

#### Step by Step

- Open 'Developer Command Prompt for VS 2017'.
- Execute `custom-dir.bat` to set up environment variables.
- Execute `python .\build-rdkit-csharp.py --build_freetype --build_platform all` to make freetype.
- Execute `python .\build-rdkit-csharp.py --build_rdkit --build_platform all` to patch rdkit and make it.
- Execute `python .\build-rdkit-csharp.py --build_wrapper` to make rdkit .NET wrapper and patch it.
- C&#35; project file is created in `(RDKit-directory)/Code/JavaWrappers/csharp_wrapper/RDKit2DotNet.csproj`.
- Execute `python .\build-rdkit-csharp.py --build_nuget` to make nuget package.
