using GraphMolWrap;

namespace RDKit
{
    public static partial class Chem
    {
        public static RWMol Mol()
        {
            return new RWMol();
        }

        public static RWMol Mol(ROMol mol)
        {
            return new RWMol(mol);
        }
    }
}
