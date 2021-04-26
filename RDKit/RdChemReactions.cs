using GraphMolWrap;

namespace RDKit
{
    public static partial class Chem
    {
        // CartesianProductStrategy
        // Compute2DCoordsForReaction
        // CreateDifferenceFingerprintForReaction
        // CreateStructuralFingerprintForReaction
        // EnumerateLibraryCanSerialize
        // GetChemDrawRxnAdjustParams
        // GetDefaultAdjustParams
        // HasAgentTemplateSubstructMatch
        // HasProductTemplateSubstructMatch
        // HasReactantTemplateSubstructMatch
        // HasReactionAtomMapping
        // HasReactionSubstructMatch
        // IsReactionTemplateMoleculeAgent
        // MatchOnlyAtRgroupsAdjustParams
        // PreprocessReaction
        // ReactionFromMolecule
        // ReactionFromPNGFile
        // ReactionFromPNGString
        // ReactionMetadataToPNGFile
        // ReactionMetadataToPNGString
        // ReactionToMolecule
        // ReactionToSmiles
        // RemoveMappingNumbersFromReactions
        // SanitizeRxn
        // UpdateProductsStereochemistry

        public static void Compute2DCoordsForReaction(ChemicalReaction rxn, double spacing = 2.0, bool updateProps = true, bool canonOrient = true, int nFlipsPerSample = 0, int nSamples = 0, int sampleSeed = 0)
            => RDKFuncs.compute2DCoordsForReaction(rxn, spacing, updateProps, canonOrient, (uint)nFlipsPerSample, (uint)nSamples, sampleSeed);

        public static ChemicalReaction ReactionFromPNGFile(string filename)
            => RDKFuncs.PNGFileToChemicalReaction(filename);

        public static ChemicalReaction PNGStringToChemicalReaction(string data)
            => RDKFuncs.PNGStringToChemicalReaction(data);

        public static ChemicalReaction ReactionFromRxnBlock(string block)
            => ChemicalReaction.ReactionFromRxnBlock(block);

        public static ChemicalReaction ReactionFromRxnFile(string filename)
            => ChemicalReaction.ReactionFromRxnFile(filename);

        public static ChemicalReaction ReactionFromSmarts(string sma, bool useSmiles = false)
            => ChemicalReaction.ReactionFromSmarts(sma, useSmiles);

        public static string ReactionToRxnBlock(ChemicalReaction rxn)
             => ChemicalReaction.ReactionToRxnBlock(rxn);

        public static string ReactionToSmarts(ChemicalReaction rxn)
            => ChemicalReaction.ReactionToSmarts(rxn);

        public static ROMol ReduceProductToSideChains(ROMol product, bool addDummyAtoms = true)
            => ChemicalReaction.ReduceProductToSideChains(product, addDummyAtoms);
    }
}
