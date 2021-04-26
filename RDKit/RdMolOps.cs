using GraphMolWrap;
using System.Collections.Generic;
using System.Linq;


namespace RDKit
{
    public static partial class Chem
    {
        //
        // rdmolops 
        //

        public struct FingerprintEnv
        {
            public ROMol submol;
            //highlightAtoms', 'atomColors', 'highlightBonds', 'bondColors', 'highlightRadii'))
        }

        //static FingerprintEnv _GetMorganEnv(
        //    ROMol mol,
        //    int atomId,
        //    double radius,
        //    double baseRad,
        //    aromaticColor, ringColor, centerColor, extraColor)
        //{
        //    if (mol.GetNumConformers() > 0)
        //    {
        //        Chem.Compute2DCoords()

        //    }
        //}

        //            if (mol.
        //            if not mol.GetNumConformers():
        //    rdDepictor.Compute2DCoords(mol)
        //  bitPath = Chem.FindAtomEnvironmentOfRadiusN(mol, radius, atomId)

        //  # get the atoms for highlighting
        //        atomsToUse = set((atomId, ))
        //  for b in bitPath:
        //    atomsToUse.add(mol.GetBondWithIdx(b).GetBeginAtomIdx())
        //    atomsToUse.add(mol.GetBondWithIdx(b).GetEndAtomIdx())

        //  #  enlarge the environment by one further bond
        //  enlargedEnv = set()
        //  for atom in atomsToUse:
        //    a = mol.GetAtomWithIdx(atom)
        //    for b in a.GetBonds():
        //      bidx = b.GetIdx()
        //      if bidx not in bitPath:
        //        enlargedEnv.add(bidx)
        //  enlargedEnv = list(enlargedEnv)
        //  enlargedEnv += bitPath

        //# set the coordinates of the submol based on the coordinates of the original molecule
        //  amap = { }
        //  submol = Chem.PathToSubmol(mol, enlargedEnv, atomMap=amap)
        //  Chem.FastFindRings(submol)
        //  conf = Chem.Conformer(submol.GetNumAtoms())
        //  confOri = mol.GetConformer(0)
        //  for i1, i2 in amap.items():
        //    conf.SetAtomPosition(i2, confOri.GetAtomPosition(i1))
        //  submol.AddConformer(conf)
        //  envSubmol = []
        //  for i1, i2 in amap.items():
        //    for b in bitPath:
        //      beginAtom = amap[mol.GetBondWithIdx(b).GetBeginAtomIdx()]
        //      endAtom = amap[mol.GetBondWithIdx(b).GetEndAtomIdx()]
        //      envSubmol.append(submol.GetBondBetweenAtoms(beginAtom, endAtom).GetIdx())

        //  # color all atoms of the submol in gray which are not part of the bit
        //  # highlight atoms which are in rings
        //  atomcolors, bondcolors = {}, {}
        //  highlightAtoms, highlightBonds = [], []
        //        highlightRadii = {}
        //  for aidx in amap.keys():
        //    if aidx in atomsToUse:
        //      color = None
        //      if centerColor and aidx == atomId:
        //        color = centerColor
        //      elif aromaticColor and mol.GetAtomWithIdx(aidx).GetIsAromatic() :
        //        color = aromaticColor
        //      elif ringColor and mol.GetAtomWithIdx(aidx).IsInRing() :
        //        color = ringColor
        //      if color is not None:
        //        atomcolors[amap[aidx]] = color
        //        highlightAtoms.append(amap[aidx])
        //        highlightRadii[amap[aidx]] = baseRad
        //    else:
        //      #drawopt.atomLabels[amap[aidx]] = '*'
        //      submol.GetAtomWithIdx(amap[aidx]).SetAtomicNum(0)
        //      submol.GetAtomWithIdx(amap[aidx]).UpdatePropertyCache()
        //  color = extraColor
        //  for bid in submol.GetBonds():
        //    bidx = bid.GetIdx()
        //    if bidx not in envSubmol:
        //      bondcolors[bidx] = color
        //      highlightBonds.append(bidx)
        //  return FingerprintEnv(submol, highlightAtoms, atomcolors, highlightBonds, bondcolors,
        //                        highlightRadii)




        public static ROMol AddHs(
            ROMol mol,
            bool explicitOnly = false,
            bool addCoords = false,
            UInt_Vect onlyOnAtoms = null,
            bool addResidueInfo = false)
        {
            var rwmol = new RWMol(mol);
            RDKFuncs.addHs(
                rwmol,
                explicitOnly,
                addCoords,
                onlyOnAtoms,
                addResidueInfo);
            return rwmol;
        }

        public static ROMol AddHs(
            RWMol mol,
            bool explicitOnly = false,
            bool addCoords = false,
            IEnumerable<int> onlyOnAtoms = null,
            bool addResidueInfo = false)
        {
            return AddHs(mol, explicitOnly, addCoords, new UInt_Vect(onlyOnAtoms.Cast<uint>()), addResidueInfo);
        }

        public static void AddRecursiveQueries(ROMol mol, StringMolMap queries, string propName)
        {
            RDKFuncs.addRecursiveQueries(mol, queries, propName);
        }

        public static void AssignChiralTypesFromBondDirs(ROMol mol, int confId = -1, bool replaceExistingTags = true)
        {
            RDKFuncs.assignChiralTypesFromBondDirs(mol, confId, replaceExistingTags);
        }

        public static void AssignRadicals(RWMol mol)
        {
            RDKFuncs.assignRadicals(mol);
        }

        public static void AssignStereochemistry(ROMol mol,
            bool cleanIt = false, bool force = false, bool flagPossibleStereoCenters = false)
        {
            RDKFuncs.assignStereochemistry(mol, cleanIt, force, flagPossibleStereoCenters);
        }

        public static void CleanUp(RWMol mol)
        {
            RDKFuncs.cleanUp(mol);
        }

        public static ROMol DeleteSubstructs(ROMol mol, ROMol query, bool onlyFrags = false, bool useChirality = false)
        {
            return RDKFuncs.deleteSubstructs(mol, query, onlyFrags, useChirality);
        }

        public static void DetectBondStereochemistry(ROMol mol, int confId = -1)
        {
            RDKFuncs.detectBondStereochemistry(mol, confId);
        }

        public static MolSanitizeException_Vect DetectChemistryProblems(ROMol mol, SanitizeFlags sanitizeOps = SanitizeFlags.SANITIZE_ALL)
        {
            return RDKFuncs.detectChemistryProblems(mol, (int)sanitizeOps);
        }

        public static void FastFindRings(ROMol mol)
        {
            RDKFuncs.fastFindRings(mol);
        }

        public static Int_Vect_List FindAllPathsOfLengthN(
            ROMol mol,
            int targetLen,
            bool useBonds = true,
            bool useHs = false,
            int rootedAtAtom = -1)
        {
            return RDKFuncs.findAllPathsOfLengthN(mol, (uint)targetLen, useBonds, useHs, rootedAtAtom);
        }

        public static Int_Int_Vect_List_Map FindAllSubgraphsOfLengthMToN(
            ROMol mol,
            int lowerLen,
            int upperLen,
            bool useHs = false,
            int rootedAtAtom = -1)
        {
            return RDKFuncs.findAllSubgraphsOfLengthsMtoN(mol, (uint)lowerLen, (uint)upperLen, useHs, rootedAtAtom);
        }

        public static Int_Vect_List FindAllSubgraphsOfLengthN(
            ROMol mol,
            int targetLen,
            bool useHs = false,
            int rootedAtAtom = -1)
        {
            return RDKFuncs.findAllSubgraphsOfLengthN(mol, (uint)targetLen, useHs, rootedAtAtom);
        }

        public static Int_Vect FindAtomEnvironmentOfRadiusN(ROMol mol, int radius, int rootedAtAtom, bool useHs = false)
        {
            return RDKFuncs.findAtomEnvironmentOfRadiusN(mol, (uint)radius, (uint)rootedAtAtom, useHs);
        }

        public static void FindPotentialStereoBonds(ROMol mol, bool cleanIt = false)
        {
            RDKFuncs.findPotentialStereoBonds(mol, cleanIt);
        }

        public static Int_Vect_List FindUniqueSubgraphsOfLengthNfindUniqueSubgraphsOfLengthN(ROMol mol, int targetLen,
            bool useHs = false, bool useBO = true, int rootedAtAtom = -1)
        {
            return RDKFuncs.findUniqueSubgraphsOfLengthN(mol, (uint)targetLen, useHs, useBO, rootedAtAtom);
        }

        public static ROMol FragmentOnBRICSBonds(ROMol mol)
        {
            return RDKFuncs.fragmentOnBRICSBonds(mol);
        }

        public static SWIGTYPE_p_double Get3DDistanceMatrix(ROMol mol,
            int confId = -1, bool useAtomWts = false, bool force = false, string propNamePrefix = "")
        {
            return RDKFuncs.get3DDistanceMat(mol, confId, useAtomWts, force, propNamePrefix);
        }

        public static SWIGTYPE_p_double GetAdjacencyMatrix(ROMol mol,
            bool useBO = false, int emptyVal = 0, bool force = false, string propNamePrefix = "")
        {
            return RDKFuncs.getAdjacencyMatrix(mol, useBO, emptyVal, force, propNamePrefix);
        }

        public static SWIGTYPE_p_double GetDistanceMatrix(ROMol mol,
            bool useBO = false, bool useAtomWts = false, bool force = false, string propNamePrefix = "")
        {
            return RDKFuncs.getDistanceMat(mol, useBO, useAtomWts, force, propNamePrefix);
        }

        public static int GetFormalCharge(ROMol mol)
        {
            return RDKFuncs.getFormalCharge(mol);
        }

        public static ROMol_Vect GetMolFrags(ROMol mol,
            bool sanitizeFrags = false, Int_Vect frags = null, Int_Vect_Vect fragsMolAtomMapping = null)
        {
            return RDKFuncs.getMolFrags(mol, sanitizeFrags, frags, fragsMolAtomMapping);
        }

        public static int GetSSSR(ROMol mol)
        {
            return RDKFuncs.findSSSR(mol);
        }

        public static Int_List GetShortestPath(ROMol mol, int aid1, int aid2)
        {
            return RDKFuncs.getShortestPath(mol, aid1, aid2);
        }

        public static int GetSymmSSSR(ROMol mol)
        {
            return RDKFuncs.symmetrizeSSSR(mol);
        }

        public static void Kekulize(RWMol mol, bool clearAromaticFlags = false)
        {
            RDKFuncs.Kekulize(mol, clearAromaticFlags);
        }

        public static ExplicitBitVect LayeredFingerprint(
            ROMol mol,
            LayerFlags layerFlags = (LayerFlags)(-1),
            int minPath = 1,
            int maxPath = 7,
            int fpSize = 2048,
            UInt_Vect atomCounts = null,
            ExplicitBitVect setOnlyBits = null,
            bool branchedPaths = true,
            UInt_Vect fromAtoms = null)
        {
            return RDKFuncs.LayeredFingerprintMol(mol, (uint)layerFlags, (uint)minPath, (uint)maxPath, (uint)fpSize, atomCounts, setOnlyBits, branchedPaths, fromAtoms);
        }

        public static ROMol MergeQueryHs(ROMol mol, bool mergeUnmappedOnly = false)
        {
            return RDKFuncs.mergeQueryHs(mol, mergeUnmappedOnly);
        }

        public static void MolAddRecursiveQueries(ROMol mol, StringMolMap queries, string propName)
        {
            RDKFuncs.addRecursiveQueries(mol, queries, propName);
        }

        public static string MolToSVG(
            ROMol mol,
            int width = 300, int height = 300,
            Int_Vect highlightAtoms = null,
#pragma warning disable IDE0079 // Remove unnecessary suppression
#pragma warning disable IDE0060 // Remove unused parameter
            bool kekulize = true,
#pragma warning restore IDE0060 // Remove unused parameter
#pragma warning restore IDE0079 // Remove unnecessary suppression
            int lineWidthMult = 1,
            int fontSize = 12,
            bool includeAtomCircles = true,
            int confId = -1)
        {
            // See Code/GraphMol/MolDraw2D/Wrap/rdMolDraw2D.cpp::molToSVG
            var drawer = new MolDraw2DSVG(width, height);
            drawer.setFontSize(fontSize / 24.0);
            drawer.setLineWidth(drawer.lineWidth() * lineWidthMult);
            drawer.drawOptions().circleAtoms = includeAtomCircles;
            drawer.drawMolecule(mol, highlightAtoms, null, null, confId);
            drawer.finishDrawing();
            return drawer.getDrawingText();
        }

        public static ROMol MurckoDecompose(ROMol mol)
        {
            return RDKFuncs.MurckoDecompose(mol);
        }

        public static StringMolMap ParseMolQueryDefFile(string filename,
            bool standardize = true, string delimiter = "\t", string comment = "//",
            int nameColumn = 0, int smartsColumn = 1)
        {
            var queryDefs = new StringMolMap();
            RDKFuncs.parseQueryDefFile(filename, queryDefs, standardize, delimiter, comment, (uint)nameColumn, (uint)smartsColumn);
            return queryDefs;
        }

        public static ROMol PathToSubmol(ROMol mol, Int_Vect path, bool useQuery = false, Int_Int_Map atomIdxMap = null)
        {
            return RDKFuncs.pathToSubmol(mol, path, useQuery, atomIdxMap);
        }

        public static ExplicitBitVect PatternFingerprint(ROMol mol,
            int fpSize = 2048, UInt_Vect atomCounts = null, ExplicitBitVect setOnlyBits = null)
        {
            return RDKFuncs.PatternFingerprintMol(mol, (uint)fpSize, atomCounts, setOnlyBits);
        }

        public static ExplicitBitVect RDKFingerprint(ROMol mol,
            int minPath = 1, int maxPath = 7, int fpSize = 2048, int nBitsPerHash = 2,
            bool useHs = true, double tgtDensity = 0, int minSize = 128, bool branchedPaths = true,
            bool useBondOrder = true, UInt_Vect atomInvariants = null, UInt_Vect fromAtoms = null,
            SWIGTYPE_p_std__vectorT_std__vectorT_uint32_t_t_t atomBits = null,
            SWIGTYPE_p_std__mapT_unsigned_int_std__vectorT_std__vectorT_int_t_t_std__lessT_unsigned_int_t_t bitInfo = null)
        {
            return RDKFuncs.RDKFingerprintMol(mol, (uint)minPath, (uint)maxPath, (uint)fpSize, (uint)nBitsPerHash, useHs, tgtDensity, (uint)minSize, branchedPaths, useBondOrder, atomInvariants, fromAtoms, atomBits, bitInfo);
        }

        public static ROMol RemoveAllHs(ROMol mol, bool sanitize = true)
        {
            return RDKFuncs.removeAllHs(mol, sanitize);
        }

        public static ROMol RemoveHs(ROMol mol,
            bool implicitOnly = false, bool updateExplicitCount = false, bool sanitize = true)
        {
            return RDKFuncs.removeHs(mol, implicitOnly, updateExplicitCount, sanitize);
        }

        public static void RemoveStereochemistry(ROMol mol)
        {
            RDKFuncs.removeStereochemistry(mol);
        }

        public static ROMol RenumberAtoms(ROMol mol, UInt_Vect newOrder)
        {
            return RDKFuncs.renumberAtoms(mol, newOrder);
        }

        public static ROMol ReplaceCore(ROMol mol, ROMol coreQuery,
            bool replaceDummies = true, bool labelByIndex = false, bool requireDummyMatch = false, bool useChirality = false)
        {
            return RDKFuncs.replaceCore(mol, coreQuery, replaceDummies, labelByIndex, requireDummyMatch, useChirality);
        }

        public static ROMol ReplaceSidechains(ROMol mol, ROMol coreQuery, bool useChirality = false)
        {
            return RDKFuncs.replaceSidechains(mol, coreQuery, useChirality);
        }

        public static ROMol_Vect ReplaceSubstructs(
            ROMol mol,
            ROMol query,
            ROMol replacement,
            bool replaceAll = false,
            int replacementConnectionPoint = 0,
            bool useChirality = false)
        {
            return RDKFuncs.replaceSubstructs(mol, query, replacement, replaceAll, (uint)replacementConnectionPoint, useChirality);
        }

        public static SanitizeFlags SanitizeMol(RWMol mol, SanitizeFlags sanitizeOps = SanitizeFlags.SANITIZE_ALL)
        {
            return (SanitizeFlags)RDKFuncs.sanitizeMol(mol, (int)sanitizeOps);
        }

        public static void SetAromaticity(RWMol mol, AromaticityModel model = AromaticityModel.AROMATICITY_DEFAULT)
        {
            RDKFuncs.setAromaticity(mol, model);
        }

        public static void SetBondStereoFromDirections(ROMol mol)
        {
            RDKFuncs.setBondStereoFromDirections(mol);
        }

        public static void SetConjugation(ROMol mol)
        {
            RDKFuncs.setConjugation(mol);
        }

        public static void SetDoubleBondNeighborDirections(ROMol mol, Conformer conf = null)
        {
            RDKFuncs.setDoubleBondNeighborDirections(mol, conf);
        }

        public static void SetHybridization(ROMol mol)
        {
            RDKFuncs.setHybridization(mol);
        }

        public static void WedgeMolBonds(ROMol mol, Conformer conf)
        {
            mol.WedgeMolBonds(conf);
        }
    }
}
