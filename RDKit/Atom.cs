using GraphMolWrap;
using System.Collections.Generic;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        public static string DescribeQuery(this Atom atom)
            => RDKFuncs.describeQuery(atom);

        public static int GetAtomMapNum(this Atom atom)
            => atom.GetAtomMapNum();

        public static int GetAtomicNum(this Atom atom)
            => atom.getAtomicNum();

        public static Bond_Vect GetBonds(this Atom atom)
            => atom.getBonds();

        public static Atom.ChiralType GetChiralTag(this Atom atom)
            => atom.getChiralTag();

        public static int GetDegree(this Atom atom)
            => (int)atom.getDegree();

        public static int GetExplicitValence(this Atom atom)
            => atom.getExplicitValence();

        public static Atom.HybridizationType GetHybridization(this Atom atom)
            => atom.getHybridization();

        public static int GetIdx(this Atom atom)
            => (int)atom.getIdx();

        public static int GetImplicitValence(this Atom atom)
            => atom.getImplicitValence();

        public static int GetIntProp(this Atom atom, string key)
            => (int)atom.getUIntProp(key);

        public static bool GetIsAromatic(this Atom atom)
            => atom.getIsAromatic();

        public static int GetIsotope(this Atom atom)
            => (int)atom.getIsotope();

        public static double GetMass(this Atom atom)
            => atom.getMass();

        public static AtomMonomerInfo GetMonomerInfo(this Atom atom)
            => atom.getMonomerInfo();

        public static IList<Atom> GetNeighbors(this Atom atom)
        {
            var parent = atom.getOwningMol();
            return parent.getAtomNeighbors(atom);
        }

        public static bool GetNoImplicit(this Atom atom)
            => atom.getNoImplicit();

        public static int GetNumExplicitHs(this Atom atom)
            => (int)atom.getNumExplicitHs();

        public static int GetNumImplicitHs(this Atom atom)
            => (int)atom.getNumImplicitHs();

        public static int GetNumRadicalElectrons(this Atom atom)
            => (int)atom.getNumRadicalElectrons();

        public static ROMol GetOwningMol(this Atom atom)
            => atom.getOwningMol();

        public static int GetPerturbationOrder(this Atom atom, Int_List probe)
            => atom.getPerturbationOrder(probe);

        public static string GetSmarts(this Atom atom, bool doKekule = false, bool allHsExplicit = false, bool isomericSmiles = true)
        {
            if (atom.hasQuery())
            {
                return RDKFuncs.GetAtomSmarts((QueryAtom)atom);
            }
            else
            {
                return RDKFuncs.GetAtomSmiles(atom, doKekule, null, allHsExplicit, isomericSmiles);
            }
        }

        public static string GetSymbol(this Atom atom)
            => atom.getSymbol();

        public static int GetTotalDegree(this Atom atom)
            => (int)atom.getTotalDegree();

        public static int GetTotalNumHs(this Atom atom, bool includeNeighbors = false)
            => (int)atom.getTotalNumHs(includeNeighbors);

        public static int GetTotalValence(this Atom atom)
            => (int)atom.getTotalValence();

        public static bool HasOwningMol(this Atom atom)
            => atom.hasOwningMol();

        public static bool HasQuery(this Atom atom)
            => atom.hasQuery();

        public static void InvertChirality(this Atom atom)
            => atom.invertChirality();

        public static bool IsInRing(this Atom atom)
            => atom.IsInRing();

        public static bool IsInRingSize(this Atom atom, int size)
            => atom.IsInRingSize(size);

        public static void MarkConjAtomBonds(this Atom atom)
            => atom.markConjAtomBonds();

        // Match

        public static bool NeedsUpdatePropertyCache(this Atom atom)
            => atom.needsUpdatePropertyCache();

        public static void SetAtomicNum(this Atom atom, int newNum)
            => atom.setAtomicNum(newNum);

        public static void SetAtomMapNum(this Atom atom, int mapno)
            => atom.setAtomMapNum(mapno);
        public static void SetAtomMapNum(this Atom atom, int mapno, bool strict)
            => atom.setAtomMapNum(mapno, strict);

        public static void SetChiralTag(this Atom atom, Atom.ChiralType what)
            => atom.setChiralTag(what);

        public static void SetFormalCharge(this Atom atom, int what)
            => atom.setFormalCharge(what);

        public static void SetHybridization(this Atom atom, Atom.HybridizationType what)
            => atom.setHybridization(what);

        public static void SetIsAromatic(this Atom atom, bool what)
            => atom.setIsAromatic(what);

        public static void SetIsotope(this Atom atom, int what)
            => atom.setIsotope((uint)what);

        public static void SetMonomerInfo(this Atom atom, AtomMonomerInfo info)
            => atom.setMonomerInfo(info);
        public static void SetNoImplicit(this Atom atom, bool what)
            => atom.setNoImplicit(what);

        public static void SetNumExplicitHs(this Atom atom, int what)
            => atom.setNumExplicitHs((uint)what);

        public static void SetNumRadicalElectrons(this Atom atom, int num)
            => atom.setNumRadicalElectrons((uint)num);

        public static void UpdatePropertyCache(this Atom atom, bool strict = true)
            => atom.updatePropertyCache(strict);
    }
}
