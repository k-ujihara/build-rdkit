# for linux
# dotnet nuget add source PATH_TO_LOCAL_NUGET_REPO

DOTNET_VERSION=$(dotnet --version)
DOTNET_VERSION=net${DOTNET_VERSION%.*}
mkdir new_app
cd new_app
dotnet new console
dotnet add package RDKit.DotNetWrap
dotnet restore 
echo 'using System; using GraphMolWrap; var smiles = "c1ccccc1C"; var mol = RWMol.MolFromSmiles(smiles); var re_smi = RDKFuncs.MolToSmiles(mol); Console.WriteLine($"Hello toluene, {re_smi}.");' > Program.cs
dotnet build
bin/Debug/$DOTNET_VERSION/new_app
if [ "$?" != "0" ] ; then
    LD_LIBRARY_PATH=bin/Debug/$DOTNET_VERSION/runtimes/linux-x64/native:$LD_LIBRARY_PATH bin/Debug/$DOTNET_VERSION/new_app
fi
