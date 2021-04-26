using GraphMolWrap;
using System.Linq;

namespace RDKit
{
    public static partial class Chem
    {
        public static class StaticSaltRemover
        {
            private static readonly string[] SaltSmarts =
            {
                "[Cl,Br,I]",
                "[Li,Na,K,Ca,Mg]",
                "[O,N]",
                "[N](=O)(O)O",
                "[P](=O)(O)(O)O",
                "[P](F)(F)(F)(F)(F)F",
                "[S](=O)(=O)(O)O",
                "[CH3][S](=O)(=O)(O)",
                "c1cc([CH3])ccc1[S](=O)(=O)(O)",
                "[CH3]C(=O)O",
                "FC(F)(F)C(=O)O",
                "OC(=O)C=CC(=O)O",
                "OC(=O)C(=O)O",
                "OC(=O)C(O)C(O)C(=O)O",
                "C1CCCCC1[NH]C1CCCCC1",
            };

            static readonly ROMol[] saltPatterns = SaltSmarts.Select(n => RWMol.MolFromSmarts(n)).ToArray();

            public static ROMol StripMol(ROMol mol)
            {
                foreach (var query in saltPatterns)
                {
                    mol = RDKFuncs.deleteSubstructs(mol, query, true);
                }
                return mol;
            }
        }
    }
}
