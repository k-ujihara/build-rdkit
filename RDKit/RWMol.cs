using GraphMolWrap;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        //
        // RWMol
        //

        // GetMol

        public static int AddAtom(this RWMol rWMol, Atom atom)
            => (int)rWMol.addAtom(atom);

        public static int AddBond(this RWMol rWMol, int beginAtomIdx, int endAtomIdx, Bond.BondType order = Bond.BondType.UNSPECIFIED)
            => (int)rWMol.addBond((uint)beginAtomIdx, (uint)endAtomIdx, order);

        public static int AddBond(this RWMol rWMol, Atom beginAtom, Atom endAtom, Bond.BondType order = Bond.BondType.UNSPECIFIED)
            => (int)rWMol.addBond(beginAtom, endAtom, order);

        public static int AddBond(this RWMol rWMol, Bond bond)
            => (int)rWMol.addBond(bond);

        public static void RemoveAtom(this RWMol rWMol, int idx)
            => rWMol.removeAtom((uint)idx);
        public static void RemoveAtom(this RWMol rWMol, Atom atom)
            => rWMol.removeAtom(atom);

        public static void RemoveBond(this RWMol rWMol, int beginAtomIdx, int endAtomIdx)
            => rWMol.removeBond((uint)beginAtomIdx, (uint)endAtomIdx);

        public static void ReplaceAtom(this RWMol rWMol, int idx, Atom atom, bool updateLabel = false, bool preserveProps = false)
            => rWMol.replaceAtom((uint)idx, atom, updateLabel, preserveProps);

        public static void ReplaceBond(this RWMol rWMol, int idx, Bond bond, bool preserveProps = false)
            => rWMol.replaceBond((uint)idx, bond, preserveProps);

        public static void SanitizeMol(this RWMol rWMol)
            => rWMol.sanitizeMol();
        public static void SetActiveAtom(this RWMol rWMol, int idx)
            => rWMol.setActiveAtom((uint)idx);
        public static void SetActiveAtom(this RWMol rWMol, Atom atom)
            => rWMol.setActiveAtom(atom);

        public static void SetStereoGroups(this RWMol rWMol, StereoGroup_Vect stereo_groups)
            => rWMol.setStereoGroups(stereo_groups);
    }
}
