# RDKit for .NET Framework

- This library is .NET framework wrapper of RDKit.
- NuGet package is available at [https://www.nuget.org/packages/RDKit.DotNetWrap/](https://www.nuget.org/packages/RDKit.DotNetWrap/).

- Example codes are in `RDKit2DotNet.Example` directory.

- Registered NuGet package was built using the following versions.
  - [RDKit Release_2019.09.1](https://github.com/rdkit/rdkit/releases/tag/Release_2019_09_1)
  - [Boost 1.74.0](https://sourceforge.net/projects/boost/files/boost-binaries/1.74.0/)
  - [Eigen 3.3.8](https://gitlab.com/libeigen/eigen/-/releases/3.3.8)
  - [zlib 1.2.11](https://zlib.net/zlib-1.2.11.tar.gz)
  - [Python](https://www.python.org/) 3.7.9
  - [CMAKE](https://cmake.org/) 3.12.18081601-MSVC_2
  - [SWIG](http://www.swig.org/) 4.0.2
  - [NuGet](https://nuget.org) 5.3.1
  - Visual Studio 2017

## How to Build

### Preparation

- Use Windows 10 (x64).
- Install Visual Studio 2017 enabling C++ and C#.
- Install CMAKE and add installed directory to PATH.
- Install Python into _default folder_ enabling pip using offical installer.
- Download the following source archives and extract them here.
  - [RDKit](hhttps://github.com/rdkit/rdkit/) to `rdkit-Release_####_##_#`  
  - [Eigen3](http://eigen.tuxfamily.org/) to `eigen-#.#.#`
  - [zlib](http://zlib.net/) to `zlib-#.#.##`
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
- Execute `build-csharp-all.bat`.
  - Procedure to build them step by step is described below.

#### Build assembly

- Open 'Developer Command Prompt for VS 2017'.
- Execute `set BUILDPLATFORM=x64` or `set BUILDPLATFORM=x86`.
- Execute `set-envs.bat`.
- Execute `make-zlib.bat`.
- Execute `python build-rdkit-csharp.py`.
- Close 'Developer Command Prompt for VS 2017'.
- C&#35; project file is created in `(RDKit-directory)/Code/JavaWrappers/csharp_wrapper/RDKit2DotNet.csproj`.
- Modify the project's codes or customize `build-rdkit-csharp.py` if required.
- To execute `RDKit2DotNet.dll`, do the followings.
  - Add the directory containing Boost DLLs to `Path`, or copy all Boost DLLs into the same directory of `RDKFuncs.dll`.
  - Set environmental variable `RDBASE` proper value if necessary.

#### Build NuGet package

- Build assemblies for both x64 and x86 according to above procedure.
- Execute `set-envs.bat`.
- Execute `build-nuget-csharp.py`.
- NuGet package is created as `(RDKit-directory)/Code/JavaWrappers/csharp_wrapper/RDKit.DotNetWrap.#.#.#.nupkg`.
