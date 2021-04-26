using GraphMolWrap;

namespace RDKit
{
    /// <summary>
    /// rdkit.Chem.Crippen module
    /// </summary>
    public static class Crippen
    {
        public static double MolLogP(ROMol mol)
        {
            return RDKFuncs.calcMolLogP(mol);
        }

        public static double MolMR(ROMol mol)
        {
            return RDKFuncs.calcMolMR(mol);
        }
    }
}
