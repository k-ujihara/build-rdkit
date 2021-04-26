using GraphMolWrap;
namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        public static void Enumerate(this ResonanceMolSupplier resonanceMolSupplier)
            => resonanceMolSupplier.enumerate();
        public static int GetAtomConjGrpIdx(this ResonanceMolSupplier resonanceMolSupplier, int ai)
            => resonanceMolSupplier.getAtomConjGrpIdx((uint)ai);
        public static int GetBondConjGrpIdx(this ResonanceMolSupplier resonanceMolSupplier, int bi)
            => resonanceMolSupplier.getBondConjGrpIdx((uint)bi);
        public static bool GetIsEnumerated(this ResonanceMolSupplier resonanceMolSupplier)
            => resonanceMolSupplier.getIsEnumerated();
        public static int GetNumConjGrps(this ResonanceMolSupplier resonanceMolSupplier)
            => (int)resonanceMolSupplier.getNumConjGrps();
        public static ResonanceMolSupplierCallback GetProgressCallback(this ResonanceMolSupplier resonanceMolSupplier)
            => resonanceMolSupplier.getProgressCallback();

        // GetSubstructMatch

        public static Match_Vect_Vect GetSubstructMatches(this ResonanceMolSupplier resonanceMolSupplier, ROMol query, bool uniquify = false, bool useChirality = false, int numThreads = 1)
            => resonanceMolSupplier.getSubstructMatches(query, uniquify, useChirality, numThreads);

        public static void SetNumThreads(this ResonanceMolSupplier resonanceMolSupplier)
            => resonanceMolSupplier.setNumThreads();

        public static void SetNumThreads(this ResonanceMolSupplier resonanceMolSupplier, int numThreads)
            => resonanceMolSupplier.setNumThreads(numThreads);

        public static void SetProgressCallback(this ResonanceMolSupplier resonanceMolSupplier, ResonanceMolSupplierCallback callback)
            => resonanceMolSupplier.setProgressCallback(callback);

        public static bool WasCanceled(this ResonanceMolSupplier resonanceMolSupplier)
            => resonanceMolSupplier.wasCanceled();

        public static bool AtEnd(this ResonanceMolSupplier resonanceMolSupplier)
            => resonanceMolSupplier.atEnd();
        public static void Reset(this ResonanceMolSupplier resonanceMolSupplier)
            => resonanceMolSupplier.reset();

        // ResonanceMolSupplierCallback

        public static int GetMaxStructures(this ResonanceMolSupplierCallback resonanceMolSupplierCallback)
            => (int)resonanceMolSupplierCallback.getMaxStructures();

        public static int GetNumConjGrps(this ResonanceMolSupplierCallback resonanceMolSupplierCallback)
            => (int)resonanceMolSupplierCallback.getNumConjGrps();

        public static int GetNumDiverseStructures(this ResonanceMolSupplierCallback resonanceMolSupplierCallback, int conjGrpIdx)
            => (int)resonanceMolSupplierCallback.getNumDiverseStructures((uint)conjGrpIdx);

        public static int GetNumStructures(this ResonanceMolSupplierCallback resonanceMolSupplierCallback, int conjGrpIdx)
            => (int)resonanceMolSupplierCallback.getNumStructures((uint)conjGrpIdx);

        // RingInfo

        public static int AddRing(this RingInfo ringInfo, Int_Vect atomIndices, Int_Vect bondIndices)
            => (int)ringInfo.addRing(atomIndices, bondIndices);

        // AreRingFamiliesInitialized
        // AtomRingFamilies

        public static Int_Vect_Vect AtomRings(this RingInfo ringInfo)
            => ringInfo.atomRings();

        // BondRingFamilies

        public static Int_Vect_Vect BondRings(this RingInfo ringInfo)
            => ringInfo.bondRings();

        public static bool IsAtomInRingOfSize(this RingInfo ringInfo, int idx, int size)
            => ringInfo.isAtomInRingOfSize((uint)idx, (uint)size);

        public static bool IsBondInRingOfSize(this RingInfo ringInfo, int idx, int size)
            => ringInfo.isBondInRingOfSize((uint)idx, (uint)size);

        public static int MinAtomRingSize(this RingInfo ringInfo, int idx)
            => (int)ringInfo.minAtomRingSize((uint)idx);

        public static int MinBondRingSize(this RingInfo ringInfo, int idx)
            => (int)ringInfo.minBondRingSize((uint)idx);

        public static int NumAtomRings(this RingInfo ringInfo, int idx)
            => (int)ringInfo.numAtomRings((uint)idx);

        public static int NumBondRings(this RingInfo ringInfo, int idx)
            => (int)ringInfo.numBondRings((uint)idx);

        public static int NumRings(this RingInfo ringInfo)
            => (int)ringInfo.numRings();
    }
}
