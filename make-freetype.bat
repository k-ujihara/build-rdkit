copy %THISDIR%freetype.vcxproj %FREETYPEDIR%\builds\windows\vc2010

@pushd %FREETYPEDIR%
cd %FREETYPEDIR%\builds\windows\vc2010

MSBuild freetype.sln /p:Configuration=Release,Platform=%MSBUILDPLATFORM% /maxcpucount
if errorlevel 1 goto :ERROREND
@popd

goto :END

:ERROREND
@echo Failed to make freetype.
exit /b 1

:END
