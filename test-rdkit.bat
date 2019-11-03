@pushd "%RDKITDIR%"
@cd "%BUILDDIR%"
MSBuild RUN_TESTS.vcxproj /p:Configuration=Release,Platform=%MSBUILDPLATFORM% /maxcpucount
@popd
