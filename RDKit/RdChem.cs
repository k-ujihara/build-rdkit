using GraphMolWrap;

namespace RDKit
{
    public static partial class Chem
    {
        //
        // rdkit.Chem.rdchem module
        //

        // ClearMolSubstanceGroups
        // CreateMolSubstanceGroup
        // CreateStereoGroup
        // FixedMolSizeMolBundle
        // GetDefaultPickleProperties
        // GetMolSubstanceGroupWithIdx
        // GetMolSubstanceGroups

        public static SubstanceGroup AddMolSubstanceGroup(ROMol mol, SubstanceGroup sgroup)
        {
            RDKFuncs.addSubstanceGroup(mol, sgroup);
            var count = RDKFuncs.getSubstanceGroupCount(mol);
            var newSubstance = RDKFuncs.getSubstanceGroupWithIdx(mol, count - 1);
            return newSubstance;
        }

        public static string GetAtomAlias(Atom atom) 
            => RDKFuncs.getAtomAlias(atom);

        public static int GetAtomRLabel(Atom atom) 
            => RDKFuncs.getAtomRLabel(atom);

        public static string GetAtomValue(Atom atom) 
            => RDKFuncs.getAtomValue(atom);

        public static PeriodicTable GetPeriodicTable() 
            => PeriodicTable.getTable();

        public static string GetSupplementalSmilesLabel(Atom atom) => RDKFuncs.getSupplementalSmilesLabel(atom);

        public static void SetAtomAlias(Atom atom, string rlabel)
            => RDKFuncs.setAtomAlias(atom, rlabel);

        public static void SetAtomRLabel(Atom atom, int rlabel)
            => RDKFuncs.setAtomRLabel(atom, rlabel);

        public static void SetAtomValue(Atom atom, string rlabel)
            => RDKFuncs.setAtomValue(atom, rlabel);

        // SetDefaultPickleProperties

        public static void SetSupplementalSmilesLabel(Atom atom, string label)
            => RDKFuncs.setSupplementalSmilesLabel(atom, label);
    }
}
