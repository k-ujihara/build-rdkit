PUSHD %RDKITDIR%
MKDIR %BUILDDIR%
CD %BUILDDIR%
@SET $EXE=cmake -DRDK_BUILD_PYTHON_WRAPPERS=ON -DBOOST_ROOT="%BOOSTDIR%\stage\%BUILDPLATFORM%" -DZLIB_LIBRARY="%ZLIBDIR%\%BUILDDIR%\Release\zlib.lib" -DZLIB_INCLUDE_DIR="%ZLIBDIR%" -DEIGEN3_INCLUDE_DIR="%EIGENDIR%" -DRDK_BUILD_INCHI_SUPPORT=ON -DRDK_BUILD_AVALON_SUPPORT=ON -G"%CMAKEG%" ..
REM Replce backslash to slash because marparser recognize backslash as escape sequence.
@SET $EXE=%$EXE:\=/%
ECHO %$EXE%
%$EXE%
@SET $EXE=
MSBuild RDKit.sln /p:Configuration=Release,Platform=%MSBUILDPLATFORM% -maxcpucount:%NUMBER_OF_PROCESSORS%
MSBuild INSTALL.vcxproj /p:Configuration=Release,Platform=%MSBUILDPLATFORM% -maxcpucount:%NUMBER_OF_PROCESSORS%
POPD
