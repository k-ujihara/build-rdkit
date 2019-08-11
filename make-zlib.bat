PUSHD %ZLIBDIR%
MKDIR %BUILDDIR%
CD %BUILDDIR%
cmake -G"%CMAKEG%" ..
MSBuild zlib.sln /p:Configuration=Release,Platform=%MSBUILDPLATFORM% -maxcpucount:%NUMBER_OF_PROCESSORS%
COPY /Y zconf.h %ZLIBDIR%
POPD
