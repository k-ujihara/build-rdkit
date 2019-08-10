pushd %RDKITDIR%
mkdir %BUILDDIR%
cd %BUILDDIR%
@SET $EXE=cmake -DRDK_BUILD_PYTHON_WRAPPERS=ON -DBOOST_ROOT="%BOOSTDIR%\stage\%MSBUILDPLATFORM%" -DZLIB_LIBRARY="%ZLIBDIR%\%BUILDDIR%\Release\zlib.lib" -DZLIB_INCLUDE_DIR="%ZLIBDIR%" -DEIGEN3_INCLUDE_DIR="%EIGENDIR%" -DRDK_BUILD_INCHI_SUPPORT=ON -DRDK_BUILD_AVALON_SUPPORT=ON -G"%CMAKEG%" ..
REM Replce backslash to slash because marparser misunderstands backslash.
@SET $EXE=%$EXE:\=/%
ECHO %$EXE%
%$EXE%
@SET $EXE=
MSBuild RDKit.sln /p:Configuration=Release,Platform=%MSBUILDPLATFORM% -maxcpucount:8
MSBuild INSTALL.vcxproj /p:Configuration=Release,Platform=%MSBUILDPLATFORM% -maxcpucount:8
popd
