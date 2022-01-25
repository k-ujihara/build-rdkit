@rem for Windows
@rem dotnet nuget add source PATH_TO_LOCAL_NUGET_REPO

for /f "DELIMS=" %A in ('dotnet --version') do set DOTNET_VERSION=%~nA
set DOTNET_VERSION=net%DOTNET_VERSION%
mkdir new_app
cd new_app
dotnet new console
dotnet add package RDKit.DotNetWrap
dotnet restore
echo using System; using GraphMolWrap; var smiles = "c1ccccc1C"; var mol = RWMol.MolFromSmiles(smiles); var re_smi = RDKFuncs.MolToSmiles(mol); Console.WriteLine($"Hello toluene, {re_smi}."); > Program.cs
dotnet build
bin\Debug\%DOTNET_VERSION%\new_app.exe
