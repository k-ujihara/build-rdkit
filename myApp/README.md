# Instruction to Build Application using RDKit.DotNetWrap

## Step by Step

```bash
mkdir new_app
cd new_app
mkdir new_app
cd new_app
dotnet new console
dotnet add package RDKit.DotNetWrap --version ${VERSION_OF_NUGET_PACKAGE}
```

Edit `Program.cs`.

```csharp
using System;
using GraphMolWrap;
var smiles = "c1ccccc1C";
var mol = RWMol.MolFromSmiles(smiles);
var re_smi = RDKFuncs.MolToSmiles(mol);
Console.WriteLine($"Hello toluene, {re_smi}.");
```

```bash
dotnet build
bin/Debug/${YOUR_DOTNET_VERSION}/new_app
```

- Above prints below.

```
Hello toluene, Cc1ccccc1.
```

- If your are using .NET Standard on Linux, setting `LD_LIBRARY_PATH` is required.

```bash
cd bin/Debug/${YOUR_DOTNET_VERSION}
LD_LIBRARY_PATH=./runtimes/linux-x64/native:$LD_LIBRARY_PATH ./new_app
```

See `create_and_run.bat` for Windows or `bash create_and_run.sh` for Linux.

## via Docker

```bash
docker build --tag IMAGE_NAME -f Dockerfile .
docker run IMAGE_NAME
```

## Appendix

Register local repository like below.

```bash
dotnet nuget add source /nuget-repo-directory --name local-repo
```
