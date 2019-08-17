PUSHD %RDKITDIR%\Code\JavaWrappers\csharp_wrapper%

MSBuild RDKit2DotNet.csproj /p:Configuration=Release,Platform=AnyCPU -maxcpucount:%NUMBER_OF_PROCESSORS%

POPD
