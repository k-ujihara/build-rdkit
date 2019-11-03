@rem Execute this file in 'Developer Command Prompt for VS 2017'.

@rem Customize set-envs.bat for your purpose.
@call set-envs.bat

@call make-zlib.bat
@call make-boost.bat
@call make-rdkit

@echo RDKit is built in '%RDKITDIR%\rdkit'. 

@call test-rdkit.bat
