using GraphMolWrap;
namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        public static double GetAbundanceForIsotope(this PeriodicTable periodicTable, int atomicNumber, int isotope)
            => periodicTable.getAbundanceForIsotope((uint)atomicNumber, (uint)isotope);

        public static double GetAbundanceForIsotope(this PeriodicTable periodicTable, string elementSymbol, int isotope)
            => periodicTable.getAbundanceForIsotope(elementSymbol, (uint)isotope);

        public static int GetAtomicNumber(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getAtomicNumber(elementSymbol);

        public static double GetAtomicWeight(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getAtomicWeight((uint)atomicNumber);

        public static double GetAtomicWeight(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getAtomicWeight(elementSymbol);

        public static int GetDefaultValence(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getDefaultValence(elementSymbol);

        public static int GetDefaultValence(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getDefaultValence((uint)atomicNumber);

        public static string GetElementSymbol(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getElementSymbol((uint)atomicNumber);

        public static double GetMassForIsotope(this PeriodicTable periodicTable, string elementSymbol, int isotope)
            => periodicTable.getMassForIsotope(elementSymbol, (uint)isotope);

        public static double GetMassForIsotope(this PeriodicTable periodicTable, int atomicNumber, int isotope)
            => periodicTable.getMassForIsotope((uint)atomicNumber, (uint)isotope);

        public static int GetMostCommonIsotope(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getMostCommonIsotope(elementSymbol);

        public static int GetMostCommonIsotope(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getMostCommonIsotope((uint)atomicNumber);

        public static double GetMostCommonIsotopeMass(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getMostCommonIsotopeMass(elementSymbol);

        public static double GetMostCommonIsotopeMass(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getMostCommonIsotopeMass((uint)atomicNumber);

        public static int GetNouterElecs(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getNouterElecs(elementSymbol);

        public static int GetNouterElecs(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getNouterElecs((uint)atomicNumber);

        public static double GetRb0(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getRb0((uint)atomicNumber);

        public static double GetRb0(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getRb0(elementSymbol);

        public static double GetRcovalent(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getRcovalent((uint)atomicNumber);

        public static double GetRcovalent(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getRcovalent(elementSymbol);

        public static double GetRvdw(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getRvdw((uint)atomicNumber);

        public static double GetRvdw(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getRvdw(elementSymbol);
        public static Int_Vect GetValenceList(this PeriodicTable periodicTable, string elementSymbol)
            => periodicTable.getValenceList(elementSymbol);

        public static Int_Vect GetValenceList(this PeriodicTable periodicTable, int atomicNumber)
            => periodicTable.getValenceList((uint)atomicNumber);
    }
}
