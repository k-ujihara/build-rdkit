# RDKit for .NET Framework

- .NET Framework wrapper of RDKit.
- NuGet package is available at [https://www.nuget.org/packages/RDKit.DotNetWrap/](https://www.nuget.org/packages/RDKit.DotNetWrap/).

- Example code is in [Program.cs](files/rdkit/RDKit2DotNetTest/Program.cs).
- See [Instruction to Build Application](myApp).

## How to Build

- Registered NuGet package was built using the following versions.
  - [RDKit Release_2021_09_4](https://github.com/rdkit/rdkit/releases/tag/Release_2021_09_4)
  - [Eigen 3.3.8](https://gitlab.com/libeigen/eigen/-/releases/3.3.8)
  - for Windows
    - [Boost 1.74.0](https://sourceforge.net/projects/boost/files/boost-binaries/1.74.0/)
    - [Cairo 1.16.0](https://www.cairographics.org/releases/cairo-1.16.0.tar.xz)
    - [libpng 1.6.37](https://sourceforge.net/projects/libpng/files/libpng16/1.6.37/libpng-1.6.37.tar.xz)
    - [pixman 0.40.0](https://www.cairographics.org/releases/pixman-0.40.0.tar.gz)
    - [zlib 1.2.11](https://zlib.net/zlib1211.zip)
    - [CMAKE 3.18.20081302-MSVC_2](https://cmake.org/)
    - Visual Studio 2019
  - [Python 3.9](https://www.python.org/)
  - [SWIG 3.0.12](http://www.swig.org/)
  - dotnet-sdk-5.0
  - for Linux
    - Ubuntu 18.04.6 LTS on WSL2

### Build Instruction

Do the following procedure.

- Build native binaries for Windows
- Build native binaries for Linux
- Build .NET wrapper
- Build NuGet package

#### Build native binaries for Windows 10 (x64)

- On Windows 10 (x64)
- Install Visual Studio 2019 enabling C++, C&#35; and CMAKE.
- Install Python version greater than 3.8.
- Install [SWIG](http://www.swig.org/).
  - IMPORTANT: SWIG-3.0 is required. SWIG-4.0 does not work.
- Make sure Python and SWIG are executable.
- Clone this repository to some directory. A name of the directory including path should be short. It is highly recommended to place it under 'C:\'.
- Download the following source archives and extract them here.
  - [RDKit](hhttps://github.com/rdkit/rdkit/) to `rdkit-Release_####_##_#`.
  - [Eigen3](http://eigen.tuxfamily.org/) to `eigen-#.#.#`.
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
- Customize `config.txt` file according to where above dependencies are installed.
- Open `Developer Command Prompt for VS 2019`.
- Execute `bash build_win.bat` to create native binaries in `$(RDKIT_DIR)/Code/JavaWrappers/csharp_wrapper/win/`.

#### Build native binaries for Ubuntu 18.4

- Don't share with Windows build.
- Ubuntu 18.4 is recommended.
- Install python 3.8 or greater, swig 3.0, and eigen3.
- Install dotnet-sdk-5.0 and Mono.
```bash
sudo wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    sudo dpkg -i packages-microsoft-prod.deb && \
    sudo rm packages-microsoft-prod.deb && \
    sudo apt-get update && \
    sudo apt-get install -y apt-transport-https && \
    sudo apt-get update && \
    sudo apt-get install -y dotnet-sdk-5.0 && \
    sudo apt-get install -y mono-mcs
```
- Clone this repository.
- Download the following source archives and extract them here.
  - [RDKit](hhttps://github.com/rdkit/rdkit/) to `rdkit-Release_####_##_#`.
- Customize `config.txt` file according to where above dependencies are installed.
- Execute `bash build_linux.sh` to create native binaries in `$(RDKIT_DIR)/Code/JavaWrappers/csharp_wrapper/linux/`.

#### Build .NET wrapper

- On Windows 10 (x64)
- Open `Developer Command Prompt for VS 2019`.
- Execute `python ./build_rdkit_csharp.py --build_wrapper` to create assembry files named `RDKit2DotNet.dll` in `$(RDKIT_DIR)\Code\JavaWrappers\csharp_wrapper\RDKit2DotNet\bin\Release\`.

#### Build and create NuGet package

- Open `Developer Command Prompt for VS 2019`.
- Copy native binaries for Linux to `$(RDKIT_DIR)/Code/JavaWrappers/csharp_wrapper/linux/`.
- Execute `python ./build_rdkit_csharp.py --build_nuget` to create NuGet package on `$(RDKIT_DIR)\Code\JavaWrappers\csharp_wrapper\RDKit2DotNet\bin\Release\`.

#### Copy created NuGet package to myApp

- Open `Developer Command Prompt for VS 2019`.
- Execute `nmake -f Makefile.win copy_to_myapp`.

### Install SWIG-3.0.12

Because RDKit's CMakeFile.txt does not work with SWIG 4.0, we need to install SWIG-3.0.

#### for Windows

Download SWIG executable from https://sourceforge.net/projects/swig/files/swigwin/swigwin-3.0.12/, extract, and add the directory to `PATH`.

#### for Linux

If SWIG-3.0 package is not availabe in your system, install it from source with the following instruction.

```
sudo apt-get update
sudo apt-get install libpcre3 libpcre3-dev
wget https://sourceforge.net/projects/swig/files/swig/swig-3.0.12/swig-3.0.12.tar.gz
tar -zxvf swig-3.0.12.tar.gz
cd swig-3.0.12
./configure
make
sudo make install
make clean
```

If you required to uninstall SWIG-4.0, do the following.

```
sudo apt-get --purge remove swig
```
