@echo off

set BUILDPLATFORM=x64
call set-envs.bat
call make-zlib.bat
python build-rdkit-csharp.py

set BUILDPLATFORM=x86
call set-envs.bat
call make-zlib.bat
python build-rdkit-csharp.py

call build-csharp-wrap.bat

python build-nuget-csharp.py
