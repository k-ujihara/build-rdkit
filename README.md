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

NuGet package is available at [https://www.nuget.org/packages/RDKit.DotNetWrap/](https://www.nuget.org/packages/RDKit.DotNetWrap/).

## How to Build

### Build for Python

- Install Visual Studio 2017 and CMAKE.
- Install Python using installer enabling pip.
- Download and extract source codes of RDKit, Boost, zlib and Eigen3 to this directory.
- Customize 'set-envs.bat' file.
- Open 'Developer Command Prompt for VS 2017'.
- Execute 'build-all.bat'.
- 'SET BUILDPLATFORM=x86' to build for 32-bit. (Some tests are failed.)

### Build for C&#35;

- Install Visual Studio 2017, CMAKE, Python and SWIG.
- Download and extract source codes of RDKit, Boost, zlib and Eigen3 to this directory.
- Customize 'set-envs.bat' file.
- Open 'Developer Command Prompt for VS 2017'.
- Execute 'SET BUILDPLATFORM=x64'.
- Execute 'set-envs.bat'.
- Execute 'python build-rdkit-csharp.py'.
- Close 'Developer Command Prompt for VS 2017'.
- Open 'Developer Command Prompt for VS 2017'.
- Execute 'SET BUILDPLATFORM=x86'.
- Execute 'set-envs.bat'.
- Execute 'python build-rdkit-csharp.py'.
- Close 'Developer Command Prompt for VS 2017'.
- C&#35; project file is created in '(RDKit-directory)/Code/JavaWrappers/csharp\_wrapper/RDKit2DotNet.csproj'.
- Set environmental variable 'RDBASE' proper value.
- Add Boost DLLs directory to 'Path', or copy all Boost DLLs into the same directory of RDKFuncs.dll.

### Build NuGet package for C&#35;

- After building for C&#35;,
- Open 'Developer Command Prompt for VS 2017'.
- Execute 'set-envs.bat'.
- Execute 'python build-rdkit-csharp.py'.
- Execute 'make-nuget-csharp.py'.
- NuGet package is created as '(RDKit-directory)/Code/JavaWrappers/csharp\_wrapper/RDKit.DotNetWrap.#.#.#.nupkg'.
- Example using this NuGet package is in 'RDKit2DotNet.Example' directory.
