set BUILDPLATFORM=x64
call :RUNTEST

set BUILDPLATFORM=x86
call :RUNTEST

goto :END

:RUNTEST
call set-envs.bat
@pushd %RDKITBUILDROOTDIR%\build%BUILDPLATFORM%CSharp
setlocal
set save_path=%path%

where freetype.dll 
if errorlevel 1 path %FREETYPEDIR%\objs\%MSBUILDPLATFORM%\Release;%path%
where RDKitGraphMol.dll
if errorlevel 1 path %RDKITDIR%\%BUILDDIRCSHARP%\bin\Release;%path%
 
ctest -j %number_of_cores% --output-on-failure -T Test

path %save_path%
endlocal
@popd
exit /b

:END
