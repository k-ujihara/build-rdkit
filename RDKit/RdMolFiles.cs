using GraphMolWrap;

namespace RDKit
{
    public static partial class Chem
    {
        //
        // rdmolfiles 
        //

        public static ForwardSDMolSupplier ForwardSDMolSupplier(string filename,
            bool sanitize = true, bool removeHs = true, bool strictParsing = true)
        {
            return new ForwardSDMolSupplier(new gzstream(filename), sanitize, removeHs, strictParsing);
        }

        public static SDMolSupplier SDMolSupplier(string fileName,
            bool sanitize = true, bool removeHs = true, bool strictParsing = true)
        {
            return new SDMolSupplier(fileName, sanitize, removeHs, strictParsing);
        }

        public static SmilesMolSupplier SmilesMolSupplier(string fileName)
        {
            return new SmilesMolSupplier(fileName);
        }

        public static TDTMolSupplier TDTMolSupplier(string fileName)
        {
            return new TDTMolSupplier(fileName);
        }

        public static TDTWriter TDTWriter(string fileName)
        {
            return new TDTWriter(fileName);
        }

        public static PDBWriter PDBWriter(string fileName, PDBFlavors flavor)
        {
            return new PDBWriter(fileName, (uint)flavor);
        }

        public static string MolFragmentToCXSmiles(ROMol mol, Int_Vect atomsToUse, Int_Vect bondsToUse = null,
            Str_Vect atomSymbols = null, Str_Vect bondSymbols = null,
            bool isomericSmiles = true, bool kekuleSmiles = false, int rootedAtAtom = -1, bool canonical = true,
            bool allBondsExplicit = false, bool allHsExplicit = false)
        {
            return RDKFuncs.MolFragmentToCXSmiles(mol, atomsToUse, bondsToUse, atomSymbols, bondSymbols, isomericSmiles, kekuleSmiles, rootedAtAtom, canonical);
        }

        public static string MolFragmentToSmarts(ROMol mol, Int_Vect atomsToUse, Int_Vect bondsToUse = null, bool isomericSmiles = true)
        {
            return RDKFuncs.MolFragmentToSmarts(mol, atomsToUse, bondsToUse, isomericSmiles);
        }

        public static string MolFragmentToSmiles(ROMol mol, Int_Vect atomsToUse, Int_Vect bondsToUse = null,
            Str_Vect atomSymbols = null, Str_Vect bondSymbols = null,
            bool isomericSmiles = true, bool kekuleSmiles = false, int rootedAtAtom = -1, bool canonical = true,
            bool allBondsExplicit = false, bool allHsExplicit = false)
        {
            return RDKFuncs.MolFragmentToSmiles(mol, atomsToUse, bondsToUse, atomSymbols, bondSymbols, isomericSmiles, kekuleSmiles, rootedAtAtom, canonical);
        }

        public static RWMol MolFromHELM(string text, bool sanitize = true)
        {
            return RWMol.MolFromHELM(text, sanitize);
        }

        public static RWMol MolFromMol2Block(string molBlock, bool sanitize = true, bool removeHs = true, bool cleanupSubstructures = true)
        {
            return RWMol.MolFromMol2Block(molBlock, sanitize, removeHs, Mol2Type.CORINA, cleanupSubstructures);
        }

        public static RWMol MolFromMol2File(string molFileName, bool sanitize = true, bool removeHs = true, bool cleanupSubstructures = true)
        {
            return RWMol.MolFromMol2File(molFileName, sanitize, removeHs, Mol2Type.CORINA, cleanupSubstructures);
        }

        // TODO: Add strictParsing
        public static RWMol MolFromMolBlock(string molBlock, bool sanitize = true, bool removeHs = true)
        {
            return RWMol.MolFromMolBlock(molBlock, sanitize, removeHs);
        }

        // TODO: Add strictParsing
        public static RWMol MolFromMolFile(string molFileName, bool sanitize = true, bool removeHs = true)
        {
            return RWMol.MolFromMolFile(molFileName, sanitize, removeHs);
        }

        public static RWMol MolFromPDBFile(string molFileName, bool sanitize = true,
            bool removeHs = true, PDBFlavors flavor = 0, bool proximityBonding = true)
        {
            return RWMol.MolFromPDBBlock(molFileName, sanitize, removeHs, (uint)flavor, proximityBonding);
        }

        public static RWMol MolFromSequence(string svg, bool sanitize = true, bool removeHs = true)
        {
            return RDKFuncs.RDKitSVGToMol(svg, sanitize, removeHs);
        }

        public static RWMol MolFromSequence(string text, bool sanitize = true, SequenceFlavor flavor = 0)
        {
            return RWMol.MolFromSequence(text, sanitize, (int)flavor);
        }

        public static RWMol MolFromSmiles(string smiles, bool sanitize = true)
        {
            return RWMol.MolFromSmiles(smiles, 0, sanitize);
        }

        public static RWMol MolFromSmarts(string smiles, bool mergeHs = false)
        {
            return RWMol.MolFromSmarts(smiles, 0, mergeHs);
        }

        public static string MolToSmarts(ROMol mol, bool isomericSmiles = true)
        {
            return RDKFuncs.MolToSmarts(mol, isomericSmiles);
        }

        public static string MolToSmiles(ROMol mol, bool isomericSmiles = true,
            bool kekuleSmiles = false, int rootedAtAtom = -1, bool canonical = true,
            bool allBondsExplicit = false, bool allHsExplicit = false, bool doRandom = false)
        {
            return RDKFuncs.MolToSmiles(mol, isomericSmiles, kekuleSmiles, rootedAtAtom, canonical, allBondsExplicit, allHsExplicit, doRandom);
        }

        public static string MolToTPLBlock(ROMol mol, string partialChargeProp = "_GasteigerCharge", bool writeFirstConfTwice = false)
        {
            return RDKFuncs.MolToTPLText(mol, partialChargeProp, writeFirstConfTwice);
        }

        public static void MolToTPLFile(ROMol mol, string filename, string partialChargeProp = "_GasteigerCharge", bool writeFirstConfTwice = false)
        {
            RDKFuncs.MolToTPLFile(mol, filename, partialChargeProp, writeFirstConfTwice);
        }

        public static string MolToMolBlock(ROMol mol, bool includeStereo = true,
            int confId = -1, bool kekulize = true, bool forceV3000 = false)
        {
            return RDKFuncs.MolToMolBlock(mol, includeStereo, confId, kekulize, forceV3000);
        }

        public static void MolToMolFile(ROMol mol, string filename, bool includeStereo = true,
            int confId = -1, bool kekulize = true, bool forceV3000 = false)
        {
            RDKFuncs.MolToMolFile(mol, filename, includeStereo, confId, kekulize, forceV3000);
        }

        public static string MolToPDBBlock(ROMol mol, int confId = -1, PDBFlavors flavor = 0)
        {
            return RDKFuncs.MolToPDBBlock(mol, confId, (uint)flavor);
        }

        public static void MolToPDBFile(ROMol mol, string filename, int confId = -1, PDBFlavors flavor = 0)
        {
            RDKFuncs.MolToPDBFile(mol, filename, confId, (uint)flavor);
        }

        public static string MolToXYZBlock(ROMol mol, int confId = -1)
        {
            return RDKFuncs.MolToXYZBlock(mol, confId);
        }

        public static void MolToXYZFile(ROMol mol, string filename, int confId = -1)
        {
            RDKFuncs.MolToXYZFile(mol, filename, confId);
        }

        public static string MolToCXSmiles(ROMol mol, bool isomericSmiles = true,
            bool kekuleSmiles = false, int rootedAtAtom = -1, bool canonical = true,
            bool allBondsExplicit = false, bool allHsExplicit = false, bool doRandom = false)
        {
            return RDKFuncs.MolToCXSmiles(mol, isomericSmiles, kekuleSmiles, rootedAtAtom, canonical, allHsExplicit, doRandom);
        }
    }
}
