set BUILDPLATFORM=x64
call :RUNTEST

set BUILDPLATFORM=x86
call :RUNTEST

goto :END

:RUNTEST
call set-envs.bat
@pushd %RDKITBUILDROOTDIR%\build%BUILDPLATFORM%CSharp
ctest -j %number_of_cores% --output-on-failure -T Test
@popd
exit /b

:END
