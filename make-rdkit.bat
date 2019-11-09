@pushd %RDKITDIR%
@mkdir %BUILDDIR%
@cd %BUILDDIR%
@setlocal
@set $EXE=cmake -DRDK_BUILD_PYTHON_WRAPPERS=ON -DPYTHON_EXECUTABLE=%PYTHONDIR%\python.exe -DBOOST_ROOT=%BOOSTDIR% -DBOOST_INCLUDEDIR=%BOOSTDIR% -DBOOST_LIBRARYDIR=%BOOSTDIR%\stage\%BUILDPLATFORM%\lib -DZLIB_LIBRARY="%ZLIBDIR%\%BUILDDIR%\Release\zlib.lib" -DZLIB_INCLUDE_DIR="%ZLIBDIR%" -DEIGEN3_INCLUDE_DIR="%EIGENDIR%" -DRDK_BUILD_INCHI_SUPPORT=ON -DRDK_BUILD_AVALON_SUPPORT=ON -G"%CMAKEG%" ..
@rem Replce backslash to slash because marparser recognize backslash as escape sequence.
@set $EXE=%$EXE:\=/%
%$EXE%
MSBuild RDKit.sln /p:Configuration=Release,Platform=%MSBUILDPLATFORM% /maxcpucount
if errorlevel 1 goto :ERROREND
MSBuild INSTALL.vcxproj /p:Configuration=Release,Platform=%MSBUILDPLATFORM% /maxcpucount
if errorlevel 1 goto :ERROREND
@set $EXE=
@endlocal
@popd

goto :END

:ERROREND
@echo Failed to make rdkit.
exit /b 1

:END
