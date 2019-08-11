PUSHD %RDKITDIR%
CD %BUILDDIR%
MSBuild RUN_TESTS.vcxproj /p:Configuration=Release,Platform=%MSBUILDPLATFORM% -maxcpucount:%NUMBER_OF_PROCESSORS%
POPD
