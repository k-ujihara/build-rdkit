using System;
using GraphMolWrap;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
            var smiles = "c1ccccc1C";
            var mol = RWMol.MolFromSmiles(smiles);
            var re_smi = RDKFuncs.MolToSmiles(mol);
            Console.WriteLine($"Hello toluene, {re_smi}.");
        }
    }
}
