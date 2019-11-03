@pushd %ZLIBDIR%
@mkdir %BUILDDIR%
@cd %BUILDDIR%
cmake -G"%CMAKEG%" ..
MSBuild zlib.sln /p:Configuration=Release,Platform=%MSBUILDPLATFORM% /maxcpucount
@copy /Y zconf.h %ZLIBDIR%
@popd
