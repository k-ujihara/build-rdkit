@echo off

call custom-dir.bat

set BUILDPLATFORM=x64
call :MAKEFORPLATFORM

set BUILDPLATFORM=x86
call :MAKEFORPLATFORM

python .\build-rdkit-csharp.py --make_native --build_platform  all
if errorlevel 1 goto :END
python .\build-rdkit-csharp.py --build_wrapper
if errorlevel 1 goto :END
python .\build-rdkit-csharp.py --build_nuget
if errorlevel 1 goto :END

goto :END

:MAKEFORPLATFORM
call set-envs.bat
call make-zlib.bat
call make-freetype.bat

exit/b

:END
