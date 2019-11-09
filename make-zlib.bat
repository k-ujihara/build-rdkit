@pushd %ZLIBDIR%
@mkdir %BUILDDIR%
@cd %BUILDDIR%
cmake -G"%CMAKEG%" ..
if errorlevel 1 goto :ERROREND
MSBuild zlib.sln /p:Configuration=Release,Platform=%MSBUILDPLATFORM% /maxcpucount
if errorlevel 1 goto :ERROREND
@copy /Y zconf.h %ZLIBDIR%
@popd

goto :END

:ERROREND
@echo Failed to make zlib.
exit /b 1

:END
