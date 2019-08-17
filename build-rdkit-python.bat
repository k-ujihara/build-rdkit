REM Execute this file in 'Developer Command Prompt for VS 2017'.

REM Customize set-envs.bat for your purpose.
CALL set-envs.bat

CALL make-zlib.bat
CALL make-boost.bat
CALL make-rdkit

ECHO RDKit is built in '%RDKITDIR%\rdkit'. 

call test-rdkit.bat
