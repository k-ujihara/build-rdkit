# Instruction to Build Application

Excecule below in this directory.

for Linux
```bash
export LD_LIBRARY_PATH=$PWD/bin/Release/net5.0/runtimes/linux-x64/native
dotnet build -c Release
bin/Release/net5.0/myApp
```

for Windows
```bat
dotnet build -c Release
bin\Release\net5.0\myApp.exe
```

Above prints below.
```
Hello toluene, Cc1ccccc1.
```
