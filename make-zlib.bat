pushd %ZLIBDIR%
mkdir %BUILDDIR%
cd %BUILDDIR%
cmake -G"%CMAKEG%" ..
MSBuild zlib.sln /p:Configuration=Release,Platform=%MSBUILDPLATFORM%
copy zconf.h %ZLIBDIR%
popd
