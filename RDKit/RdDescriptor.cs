using GraphMolWrap;
using System;
using System.Collections.Generic;

namespace RDKit
{
    public static partial class Chem
    {
        //
        // rdDescriptor
        //

        // TODO: Compute2DCoordsMimicDistmat

        public static int Compute2DCoords(
            ROMol mol,
            bool canonOrient = true,
            bool clearConfs = true,
            IReadOnlyDictionary<int, Point2D> coordMap = null,
            int nFlipsPerSample = 0,
            int nSamples = 0,
            int sampleSeed = 0,
            bool permuteDeg4Nodes = false)
        {
            // TODO: bondLength and forceRDKit option is not implemented.

            var cMap = new Int_Point2D_Map();
            var n_atoms = mol.getNumAtoms();
            if (coordMap != null)
            {
                foreach (var id in coordMap.Keys)
                {
                    if (id >= n_atoms)
                        throw new ArgumentOutOfRangeException(nameof(coordMap));
                    cMap[id] = coordMap[id];
                }
            }

            return (int)mol.compute2DCoords(cMap, canonOrient, clearConfs, (uint)nFlipsPerSample, (uint)nSamples, sampleSeed, permuteDeg4Nodes);
        }

        public static int Compute2DCoordsMimicDistmat(
            ROMol mol,
            Shared_Double_Array dmat,
            bool canonOrient = false,
            bool clearConfs = true,
            double weightDistMat = 0.5,
            int nFlipsPerSample = 3,
            int nSamples = 100,
            int sampleSeed = 100,
            bool permuteDeg4Nodes = true,
            bool forceRDKit = false)
            => (int)mol.compute2DCoordsMimicDistMat(
                dmat,
                canonOrient,
                clearConfs,
                weightDistMat,
                (uint)nFlipsPerSample,
                (uint)nSamples,
                sampleSeed,
                permuteDeg4Nodes,
                forceRDKit);

        public static void GenerateDepictionMatching2DStructure(
            ROMol mol,
            ROMol reference,
            int confId = -1,
            ROMol referencePattern = null,
            bool acceptFailure = false,
            bool forceRDKit = false)
            => mol.generateDepictionMatching2DStructure(reference, confId, referencePattern, acceptFailure, forceRDKit);

        public static void GenerateDepictionMatching3DStructure(
            ROMol mol,
            ROMol reference,
            int confId = -1,
            ROMol referencePattern = null,
            bool acceptFailure = false,
            bool forceRDKit = false)
            => RDKFuncs.generateDepictionMatching3DStructure(mol, reference, confId, referencePattern, acceptFailure, forceRDKit);

        public static void SetPreferCoordGen(bool val)
            => RDKFuncs.setPreferCoordGen(val);
    }
}
