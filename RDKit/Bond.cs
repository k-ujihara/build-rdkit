using GraphMolWrap;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        public static string DescribeQuery(this Bond bond)
            => RDKFuncs.describeQuery(bond);

        public static Atom GetBeginAtom(this Bond bond)
            => bond.getBeginAtom();

        public static int GetBeginAtomIdx(this Bond bond)
            => (int)bond.getBeginAtomIdx();

        public static Bond.BondDir GetBondDir(this Bond bond)
            => bond.getBondDir();

        public static Bond.BondType GetBondType(this Bond bond)
            => bond.getBondType();

        public static double GetBondTypeAsDouble(this Bond bond)
            => bond.getBondTypeAsDouble();

        public static Atom GetEndAtom(this Bond bond)
            => bond.getEndAtom();

        public static int GetEndAtomIdx(this Bond bond)
            => (int)bond.getEndAtomIdx();

        public static int GetIdx(this Bond bond)
            => (int)bond.getIdx();

        public static bool GetIsAromatic(this Bond bond)
            => bond.getIsAromatic();

        public static bool GetIsConjugated(this Bond bond)
            => bond.getIsConjugated();

        public static Atom GetOtherAtom(this Bond bond, Atom what)
            => bond.getOtherAtom(what);

        public static int GetOtherAtomIdx(this Bond bond, int thisIdx)
            => (int)bond.getOtherAtomIdx((uint)thisIdx);

        public static ROMol GetOwningMol(this Bond bond)
            => bond.getOwningMol();

        public static string GetSmarts(this Bond bond, bool allBondsExplicit = false)
        {
            if (bond.hasQuery())
            {
                return RDKFuncs.GetBondSmarts((QueryBond)bond);
            }
            else
            {
                return RDKFuncs.GetBondSmiles(bond, -1, false, allBondsExplicit);
            }
        }

        public static Bond.BondStereo GetStereo(this Bond bond)
            => bond.getStereo();

        public static Int_Vect GetStereoAtoms(this Bond bond)
            => bond.getStereoAtoms();

        public static bool HasOwningMol(this Bond bond)
            => bond.hasOwningMol();
        public static bool HasQuery(this Bond bond)
            => bond.hasQuery();

        public static bool IsInRing(this Bond bond)
            => bond.IsInRing();

        public static bool IsInRingSize(this Bond bond, int size)
            => bond.IsInRingSize(size);

        public static void SetBeginAtomIdx(this Bond bond, int what)
            => bond.setBeginAtomIdx((uint)what);

        // Match

        public static void SetBondDir(this Bond bond, Bond.BondDir what)
            => bond.setBondDir(what);

        public static void SetBondType(this Bond bond, Bond.BondType bT)
            => bond.setBondType(bT);

        public static void SetEndAtomIdx(this Bond bond, int what)
            => bond.setEndAtomIdx((uint)what);

        public static void SetIsAromatic(this Bond bond, bool what)
            => bond.setIsAromatic(what);

        public static void SetIsConjugated(this Bond bond, bool what)
            => bond.setIsConjugated(what);

        public static void SetStereo(this Bond bond, Bond.BondStereo what)
            => bond.setStereo(what);

        public static void SetStereoAtoms(this Bond bond, int bgnIdx, int endIdx)
            => bond.setStereoAtoms((uint)bgnIdx, (uint)endIdx);
    }
}
