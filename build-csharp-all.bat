@echo off

call custom-dir.bat

set BUILDPLATFORM=x64
call :MAKEFORPLATFORM

set BUILDPLATFORM=x86
call :MAKEFORPLATFORM

call build-csharp-wrap.bat
python build-nuget-csharp.py

goto :END

:MAKEFORPLATFORM
call set-envs.bat
call make-zlib.bat
call make-freetype.bat
python ./build-rdkit-csharp.py
exit/b

:END
