@echo off

set BUILDPLATFORM=x64
call set-envs.bat
call make-zlib.bat
call make-boost.bat
python build-rdkit-csharp.py

set BUILDPLATFORM=x86
call set-envs.bat
call make-zlib.bat
call make-boost.bat
python build-rdkit-csharp.py

set BUILDPLATFORM=

call build-csharp-wrap.bat

python build-nuget-csharp.py
