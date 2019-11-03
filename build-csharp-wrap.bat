@pushd %RDKITDIR%\Code\JavaWrappers\csharp_wrapper%
MSBuild RDKit2DotNet.csproj /p:Configuration=Release,Platform=AnyCPU /maxcpucount
@popd
