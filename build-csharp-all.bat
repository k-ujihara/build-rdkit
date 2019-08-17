SET BUILDPLATFORM=x64
CALL set-envs.bat
CALL make-zlib.bat
CALL make-boost.bat
python build-rdkit-csharp.py

SET BUILDPLATFORM=x86
CALL set-envs.bat
CALL make-zlib.bat
CALL make-boost.bat
python build-rdkit-csharp.py

CALL build-csharp-wrap.bat

python build-nuget-csharp.py

