using GraphMolWrap;
using System.Collections.Generic;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        //
        // ROMol
        //

        public static int AddConformer(this ROMol rOMol, Conformer ownedConf, bool assignId = false)
            => (int)rOMol.addConformer(ownedConf, assignId);

        public static void ComputeGasteigerCharges(this ROMol rOMol, ROMol mol, int nIter = 12, bool throwOnParamFailure = false)
            => rOMol.computeGasteigerCharges(mol, nIter, throwOnParamFailure);

        // Debug
        // GetAromaticAtoms
        // GetAtomsMatchingQuery
        // GetBonds
        public static Atom GetAtomWithIdx(this ROMol rOMol, int idx)
            => rOMol.getAtomWithIdx((uint)idx);

        public static Atom_Vect GetAtoms(this ROMol rOMol)
            => rOMol.getAtoms();
        public static Bond GetBondBetweenAtoms(this ROMol rOMol, int idx1, int idx2)
            => rOMol.getBondBetweenAtoms((uint)idx1, (uint)idx2);

        public static IEnumerable<Bond> GetBonds(this ROMol rOMol)
        {
            var n = rOMol.getNumBonds();
            for (int i = 0; i < n; i++)
                yield return rOMol.getBondWithIdx((uint)i);
        }

        public static Bond GetBondWithIdx(this ROMol rOMol, int idx)
           => rOMol.getBondWithIdx((uint)idx);

        public static Conformer GetConformer(this ROMol rOMol, int id = -1)
            => rOMol.getConformer(id);

        public static int GetNumAtoms(this ROMol rOMol, bool onlyExplicit = true)
            => (int)rOMol.getNumAtoms(onlyExplicit);

        public static int GetNumBonds(this ROMol rOMol, bool onlyHeavy = true)
            => (int)rOMol.getNumBonds(onlyHeavy);

        public static int GetNumConformers(this ROMol rOMol)
            => (int)rOMol.getNumConformers();

        public static int GetNumHeavyAtoms(this ROMol rOMol)
            => (int)rOMol.getNumHeavyAtoms();

        public static RingInfo GetRingInfo(this ROMol rOMol)
            => rOMol.getRingInfo();

        // GetStereoGroups

        public static Match_Vect GetSubstructMatch(this ROMol rOMol, ROMol query, SubstructMatchParameters ps)
            => rOMol.getSubstructMatch(query, ps);

        public static Match_Vect GetSubstructMatch(this ROMol rOMol, ROMol query, bool useChirality = false)
            => rOMol.getSubstructMatch(query, useChirality);


        public static Match_Vect_Vect GetSubstructMatches(this ROMol rOMol, ROMol query, SubstructMatchParameters ps)
            => rOMol.getSubstructMatches(query, ps);

        public static Match_Vect_Vect GetSubstructMatches(this ROMol rOMol, ROMol query, bool uniquify = true, bool useChirality = false)
            => rOMol.getSubstructMatches(query, uniquify, useChirality);

        public static bool HasSubstructMatch(this ROMol rOMol, ROMol query, bool useChirality = false)
            => rOMol.hasSubstructMatch(query, useChirality);

        public static bool HasSubstructMatch(this ROMol rOMol, ROMol query, SubstructMatchParameters ps)
            => rOMol.hasSubstructMatch(query, ps);

        public static bool NeedsUpdatePropertyCache(this ROMol rOMol)
            => rOMol.needsUpdatePropertyCache();

        public static void RemoveAllConformers(this ROMol rOMol)
        {
            var n = (int)rOMol.getNumConformers();
            for (int i = n; i >= 0; i--)
                rOMol.removeConformer((uint)i);
        }

        public static void RemoveConformer(this ROMol rOMol, int id)
            => rOMol.removeConformer((uint)id);

        public static Int_Vect ToBinary(this ROMol rOMol)
            => rOMol.ToBinary();

        public static void UpdatePropertyCache(this ROMol rOMol, bool strict = true)
            => rOMol.updatePropertyCache(strict);
    }
}
