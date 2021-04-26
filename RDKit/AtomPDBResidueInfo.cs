using GraphMolWrap;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        public static string GetAltLoc(this AtomPDBResidueInfo atomPDBResidueInfo)
            => atomPDBResidueInfo.getAltLoc();

        public static string GetChainId(this AtomPDBResidueInfo atomPDBResidueInfo)
            => atomPDBResidueInfo.getChainId();

        public static string GetInsertionCode(this AtomPDBResidueInfo atomPDBResidueInfo)
            => atomPDBResidueInfo.getInsertionCode();

        public static bool GetIsHeteroAtom(this AtomPDBResidueInfo atomPDBResidueInfo)
            => atomPDBResidueInfo.getIsHeteroAtom();

        public static double GetOccupancy(this AtomPDBResidueInfo atomPDBResidueInfo)
            => atomPDBResidueInfo.getOccupancy();

        public static string GetResidueName(this AtomPDBResidueInfo atomPDBResidueInfo)
            => atomPDBResidueInfo.getResidueName();

        public static int GetResidueNumber(this AtomPDBResidueInfo atomPDBResidueInfo)
            => atomPDBResidueInfo.getResidueNumber();

        public static int GetSecondaryStructure(this AtomPDBResidueInfo atomPDBResidueInfo)
            => (int)atomPDBResidueInfo.getSecondaryStructure();

        public static int GetSegmentNumber(this AtomPDBResidueInfo atomPDBResidueInfo)
            => (int)atomPDBResidueInfo.getSegmentNumber();

        public static int GetSerialNumber(this AtomPDBResidueInfo atomPDBResidueInfo)
            => atomPDBResidueInfo.getSerialNumber();

        public static double GetTempFactor(this AtomPDBResidueInfo atomPDBResidueInfo)
            => atomPDBResidueInfo.getTempFactor();

        public static void SetAltLoc(this AtomPDBResidueInfo atomPDBResidueInfo, string val)
            => atomPDBResidueInfo.setAltLoc(val);

        public static void SetChainId(this AtomPDBResidueInfo atomPDBResidueInfo, string val)
            => atomPDBResidueInfo.setChainId(val);

        public static void SetInsertionCode(this AtomPDBResidueInfo atomPDBResidueInfo, string val)
            => atomPDBResidueInfo.setInsertionCode(val);

        public static void SetIsHeteroAtom(this AtomPDBResidueInfo atomPDBResidueInfo, bool val)
            => atomPDBResidueInfo.setIsHeteroAtom(val);

        public static void SetOccupancy(this AtomPDBResidueInfo atomPDBResidueInfo, double val)
            => atomPDBResidueInfo.setOccupancy(val);

        public static void SetResidueName(this AtomPDBResidueInfo atomPDBResidueInfo, string val)
            => atomPDBResidueInfo.setResidueName(val);

        public static void SetResidueNumber(this AtomPDBResidueInfo atomPDBResidueInfo, int val)
            => atomPDBResidueInfo.setResidueNumber(val);

        public static void SetSecondaryStructure(this AtomPDBResidueInfo atomPDBResidueInfo, int val)
            => atomPDBResidueInfo.setSecondaryStructure((uint)val);

        public static void SetSegmentNumber(this AtomPDBResidueInfo atomPDBResidueInfo, int val)
            => atomPDBResidueInfo.setSegmentNumber((uint)val);


        public static void SetSerialNumber(this AtomPDBResidueInfo atomPDBResidueInfo, int val)
            => atomPDBResidueInfo.setSerialNumber(val);

        public static void SetTempFactor(this AtomPDBResidueInfo atomPDBResidueInfo, double val)
            => atomPDBResidueInfo.setTempFactor(val);
    }
}
