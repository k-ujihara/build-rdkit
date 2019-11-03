# RDKit for .NET Framework

NuGet package is available at [https://www.nuget.org/packages/RDKit.DotNetWrap/](https://www.nuget.org/packages/RDKit.DotNetWrap/).

Example code is in `RDKit2DotNet.Example` directory.

Newest NuGet package was built using the following versions.

- RDKit [Release_2019.09.1](https://github.com/rdkit/rdkit/releases/tag/Release_2019_09_1)
- [Boost 1.70.0](https://www.boost.org/users/history/version_1_70_0.html)
- [Eigen 3.3.7](http://bitbucket.org/eigen/eigen/get/3.3.7.tar.bz2)
- [zlib 1.2.11](https://zlib.net/zlib-1.2.11.tar.gz)
- [Python](https://www.python.org/) 3.6.8
- [CMAKE](https://cmake.org/) 3.15.5
- [SWIG](http://www.swig.org/) 4.0.1
- [NuGet](https://nuget.org) 5.3.1
- Visual Studio 2017

## How to Build

- Use Windows 10 (x64).
- Install Visual Studio 2017 enabling C++ and C#.
- Install CMAKE and add the directory to PATH.
- Install Python into _default folder_ enabling pip using offical installer. If you build for x86, Python for 32-bit is also required to install.
- Download the following source codes and extract them into each directory.
	- [RDKit](hhttps://github.com/rdkit/rdkit/) to `rdkit-Release_####_##_#`
	- [Boost](https://www.boost.org) to `boost_#_##_#`
	- [Eigen3](http://eigen.tuxfamily.org/) to `eigen-eigen-############`
	- [zlib](http://zlib.net/) to `zlib-#.#.##`
- Customize `custom-dir.bat` file according to where above dependencies are installed.
- Set `PYTHONVERSION` variable like the following if you specify Python's version.
	- `set PYTHONVERSION=Python36`
- Install SWIG, ie, extract SWIG distributalbe and add the directory to PATH if you build for .NET Framework.

### Build for Python

- Open 'Developer Command Prompt for VS 2017'.
- Execute `build-rdkit-python.bat`.
- `set BUILDPLATFORM=x86` before execution above if you build for 32-bit. (32-bit build fails several python tests.)

### Build for .NET Framework and create NuGet package

- Install Python both x86 and x64 version. They are assumed to be installed in default folder, ie, `%LOCALAPPDATA%\Programs\Python\Python##-32` and `%LOCALAPPDATA%\Programs\Python\Python##`.
- Open 'Developer Command Prompt for VS 2017'.
- Execute `build-csharp-all.bat`.
	- Procedure to build them step by step is described below.

#### Build assembly

- Open 'Developer Command Prompt for VS 2017'.
- Execute `set BUILDPLATFORM=x64` or `set BUILDPLATFORM=x86`.
- Execute `set-envs.bat`.
- Execute `make-zlib.bat`.
- Execute `make-boost.bat`.
- Execute `python build-rdkit-csharp.py`.
- Close 'Developer Command Prompt for VS 2017'.
- C&#35; project file is created in `(RDKit-directory)/Code/JavaWrappers/csharp_wrapper/RDKit2DotNet.csproj`.
- Modify the project's codes or customize `build-rdkit-csharp.py` if required.
- To execute `RDKit2DotNet.dll`, do the followings.
  - Add the directory containing Boost DLLs built in `make-boost.bat` to `Path` , or copy all Boost DLLs into the same directory of `RDKFuncs.dll`.
  - Set environmental variable `RDBASE` proper value if necessary.

#### Build NuGet package

- Build assemblies for both x64 and x86 according to above procedure.
- Execute `set-envs.bat`.
- Execute `build-nuget-csharp.py`.
- NuGet package is created as `(RDKit-directory)/Code/JavaWrappers/csharp_wrapper/RDKit.DotNetWrap.#.#.#.nupkg`.
