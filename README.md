# Build RDKit using Visual Studio 2017

This is to build RDKit for Windows with Visual Studio 2017. This is tested using the following versions.

- rdkit-Release\_2019\_03\_3
- Boost 1.70.0
- Eigen 3.3.7
- zlib 1.2.11
- Python 3.6.8
- SWIG 4.0.0
- CMAKE 3.15.1

## NuGet package

Compiled NuGet package is available at [https://www.nuget.org/packages/RDKit.DotNetWrap/](https://www.nuget.org/packages/RDKit.DotNetWrap/).

## How to Build

### Requirements

- Install Visual Studio 2017 and CMAKE.
- Install Python using installer enabling pip.
- Download and extract source codes of RDKit, Boost, zlib and Eigen3 to this directory.

### Build for Python

- Customize 'custom-dir.bat' file.
- Open 'Developer Command Prompt for VS 2017'.
- Execute 'build-python.bat'.
- 'SET BUILDPLATFORM=x86' before execution above if you build for 32-bit. (Some tests are failed.)

### Build for C&#35;

- Customize 'custom-dir.bat' file.
- Open 'Developer Command Prompt for VS 2017'.
- Execute 'build-csharp-all.bat'.
- If error happened, see below.

#### Step by Step

#### Build Assembly

- Open 'Developer Command Prompt for VS 2017'.
- Execute 'SET BUILDPLATFORM=x64' or 'SET BUILDPLATFORM=x86'.
- Execute 'set-envs.bat'.
- Execute 'make-zlib.bat'.
- Execute 'make-boost.bat'.
- Execute 'python build-rdkit-csharp.py'.
- Close 'Developer Command Prompt for VS 2017'.
- C&#35; project file is created in '(RDKit-directory)/Code/JavaWrappers/csharp\_wrapper/RDKit2DotNet.csproj'.
- Modify the project's codes or customize 'build-rdkit-csharp.py' if required.
- To execute RDKit2DotNet.dll, do the followings.
  - Set environmental variable 'RDBASE' proper value.
  - Add Boost DLLs directory to 'Path', or copy all Boost DLLs into the same directory of RDKFuncs.dll.

#### Build NuGet package for C&#35;

- Build both x64 and x86 version according to above procedure.
- Open 'Developer Command Prompt for VS 2017'.
- Execute 'set-envs.bat'.
- Execute 'build-nuget-csharp.py'.
- NuGet package is created as '(RDKit-directory)/Code/JavaWrappers/csharp\_wrapper/RDKit.DotNetWrap.#.#.#.nupkg'.
- Example using this NuGet package is in 'RDKit2DotNet.Example' directory.
