set BUILDPLATFORM=x64
call set-envs.bat
@pushd %RDKITDIR%\buildx64CSharp
ctest -j %number_of_cores% --output-on-failure -T Test
@popd

set BUILDPLATFORM=x86
call set-envs.bat
@pushd %RDKITDIR%\buildx86CSharp
ctest -j %number_of_cores% --output-on-failure -T Test
@popd
