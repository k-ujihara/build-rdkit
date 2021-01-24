# RDKit for .NET Framework

- .NET Framework wrapper of RDKit.
- NuGet package is available at [https://www.nuget.org/packages/RDKit.DotNetWrap/](https://www.nuget.org/packages/RDKit.DotNetWrap/).

- Example codes are in `RDKit2DotNet.Example` directory.

- Registered NuGet package was built using the following versions.
  - [RDKit Release_2020.09.3](https://github.com/rdkit/rdkit/releases/tag/Release_2020_09_3)
  - [Boost 1.74.0](https://sourceforge.net/projects/boost/files/boost-binaries/1.74.0/)
  - [Eigen 3.3.8](https://gitlab.com/libeigen/eigen/-/releases/3.3.8)
  - [Cairo 1.16.0](https://www.cairographics.org/releases/cairo-1.16.0.tar.xz)
  - [libpng 1.6.37](https://sourceforge.net/projects/libpng/files/libpng16/1.6.37/libpng-1.6.37.tar.xz)
  - [pixman 0.40.0](https://www.cairographics.org/releases/pixman-0.40.0.tar.gz)
  - [zlib 1.2.11](https://zlib.net/zlib1211.zip)
  - [Python 3.8.3](https://www.python.org/)
  - [CMAKE 3.12.18081601-MSVC_2](https://cmake.org/)
  - [SWIG 4.0.2](http://www.swig.org/)
  - [NuGet 5.3.1](https://nuget.org)
  - Ubuntu 18.4 on WSL2
  - Visual Studio 2019

## How to Build

### Preparation

- Use Windows 10 (x64).
- Install Ubuntu 18.4 on WSL2 and install dotnet, boost, cairo, cmake, and swig.
- Install Visual Studio 2019 enabling C++, C&#35; and CMAKE.
- Install Python.
- Clone this repository to some directory. A name of the directory including path should be short. It is highly recommended to place it under 'C:\' folder.
- Download the following source archives and extract them here.
  - [RDKit](hhttps://github.com/rdkit/rdkit/) to `rdkit-Release_####_##_#`.
  - [Eigen3](http://eigen.tuxfamily.org/) to `eigen-#.#.#`.
  - [SWIG](http://www.swig.org/) to `swigwin-#.#.#`.
  - [cairo](https://www.cairographics.org/) to `cairo-#.##.#`.
  - [pixman](https://www.cairographics.org/) to `pixman-#.##.#`.
  - [zlib](https://zlib.net/) to `zlib-#.#.##`.
  - [libpng 1.6](http://www.libpng.org/pub/png/libpng.html) to `lpng16##`.
  - [FreeType](https://www.freetype.org/) to `freetype-#.##.#`.

- Download binery archives of both 32-bit and 64-bit versions of Boost for Visual Studio 2019, ie, msvc-14.2.
  - [https://sourceforge.net/projects/boost/files/boost-binaries/](https://sourceforge.net/projects/boost/files/boost-binaries/).
  - Execute EXE files to extract. Defaults to store to `C:\local`.
  - Copy `boost_#_##_#` directory here.
  - Only dll and lib, ie, the files in `lib64-msvc-14.#` and `lib32-msvc-14.#`, are used to build.
  - After above, `lib64-msvc-14.#` and `lib32-msvc-14.#` should be created under `boost_#_##_#` directory.

- Customize `custom-dir.bat` file according to where above dependencies are installed.

### Build and create NuGet package

- Open 'Developer Command Prompt for VS 2019'.
- Execute `build_all.bat`.
  - Procedure to build them step by step is described below.

#### Step by Step

- Open 'Developer Command Prompt for VS 2019'.
- Execute `custom-dir.bat` to set up environment variables.
- Execute `python .\build_rdkit_csharp.py --build_freetype --build_platform all` to make FreeType.
- Execute `python .\build_rdkit_csharp.py --build_zlib --build_platform all` to make zlib.
- Execute `python .\build_rdkit_csharp.py --build_libpng --build_platform all` to make libpng.
- Execute `python .\build_rdkit_csharp.py --build_pixman --build_platform all` to make pixman.
- Execute `python .\build_rdkit_csharp.py --build_cairo --build_platform all` to make cairo.
- Execute `python .\build_rdkit_csharp.py --build_rdkit --build_platform all` to patch RDKit and make it.
- Execute `python .\build_rdkit_csharp.py --build_wrapper` to make rdkit .NET wrapper and patch it.
- C&#35; project file is created in `rdkit-Release_####_##_#/Code/JavaWrappers/csharp_wrapper/RDKit2DotNet.csproj`.
- Execute `python .\build_rdkit_csharp.py --build_nuget` to make NuGet package.
