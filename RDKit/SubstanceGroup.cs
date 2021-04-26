using GraphMolWrap;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        // StereoGroup

        public static Atom_Vect GetAtoms(this StereoGroup stereoGroup)
            => stereoGroup.getAtoms();

        public static StereoGroupType GetGroupType(this StereoGroup stereoGroup)
            => stereoGroup.getGroupType();

        // SubstanceGroup

        public static void AddAtomWithBookmark(this SubstanceGroup substanceGroup, int mark)
        => substanceGroup.addAtomWithBookmark(mark);

        public static void AddAtomWithIdx(this SubstanceGroup substanceGroup, int idx)
            => substanceGroup.addAtomWithIdx((uint)idx);

        public static void AddAttachPoint(this SubstanceGroup substanceGroup, int aIdx, int lvIdx, string idStr)
            => substanceGroup.addAttachPoint((uint)aIdx, lvIdx, idStr);

        public static void AddBondWithBookmark(this SubstanceGroup substanceGroup, int mark)
            => substanceGroup.addBondWithBookmark(mark);

        public static void AddBondWithIdx(this SubstanceGroup substanceGroup, int idx)
            => substanceGroup.addBondWithIdx((uint)idx);

        public static void AddBracket(this SubstanceGroup substanceGroup, SWIGTYPE_p_std__arrayT_RDGeom__Point3D_3_t bracket)
            => substanceGroup.addBracket(bracket);

        public static void AddCState(this SubstanceGroup substanceGroup, int bondIdx, Point3D vector)
            => substanceGroup.addCState((uint)bondIdx, vector);

        public static void AddParentAtomWithBookmark(this SubstanceGroup substanceGroup, int mark)
            => substanceGroup.addParentAtomWithBookmark(mark);

        public static void AddParentAtomWithIdx(this SubstanceGroup substanceGroup, int idx)
            => substanceGroup.addParentAtomWithIdx((uint)idx);

        public static Int_Vect GetAtoms(this SubstanceGroup substanceGroup)
            => substanceGroup.getAtoms();
        public static SubstanceGroup.AttachPoint GetAttachPoint(this SubstanceGroup substanceGroup, int idx)
            => substanceGroup.getAttachPoint((uint)idx);

        public static Int_Vect GetBonds(this SubstanceGroup substanceGroup)
            => substanceGroup.getBonds();

        public static SWIGTYPE_p_std__arrayT_RDGeom__Point3D_3_t GetBracket(this SubstanceGroup substanceGroup, int idx)
            => substanceGroup.getBracket((uint)idx);

        public static SubstanceGroup.CState GetCState(this SubstanceGroup substanceGroup, int idx)
            => substanceGroup.getCState((uint)idx);

        public static ROMol GetOwningMol(this SubstanceGroup substanceGroup)
            => substanceGroup.getOwningMol();

        public static UInt_Vect GetParentAtoms(this SubstanceGroup substanceGroup)
            => substanceGroup.getParentAtoms();
    }
}
