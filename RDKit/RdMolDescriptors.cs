using GraphMolWrap;
using System.Collections.Generic;
using System.Linq;
using static RDKit.GraphMolWrapTools;

namespace RDKit
{
    public static partial class Chem
    {
        // TODO:
        // GetHashedMorganFingerprint
        // MakePropertyRangeQuery

        //
        // MolDescriptors2D
        //

        public static Double_Vect BCUT2D(ROMol mol)
            => RDKFuncs.BCUT2D(mol);

        public static Double_Pair BCUT2D(ROMol mol, IReadOnlyList<double> atom_props)
            => RDKFuncs.BCUT2D(mol, new Double_Vect(atom_props));

        public static Double_Pair BCUT2D(ROMol mol, string atom_propname)
            => RDKFuncs.BCUT2D(mol, atom_propname);

        public static IReadOnlyList<double> AUTOCORR2D(ROMol mol, string customAtomPropName)
        {
            var res = new Double_Vect();
            RDKFuncs.AUTOCORR2D(mol, res, customAtomPropName);
            return res.ToList();
        }

        public static double CalcChi0n(ROMol mol, bool force = false)
            => RDKFuncs.calcChi0n(mol, force);

        public static double CalcChi0v(ROMol mol, bool force = false)
            => RDKFuncs.calcChi0v(mol, force);

        public static double CalcChi1n(ROMol mol, bool force = false)
            => RDKFuncs.calcChi1n(mol, force);

        public static double CalcChi1v(ROMol mol, bool force = false)
            => RDKFuncs.calcChi1v(mol, force);

        public static double CalcChi2n(ROMol mol, bool force = false)
            => RDKFuncs.calcChi2n(mol, force);

        public static double CalcChi2v(ROMol mol, bool force = false)
            => RDKFuncs.calcChi2v(mol, force);

        public static double CalcChi3n(ROMol mol, bool force = false)
            => RDKFuncs.calcChi3n(mol, force);

        public static double CalcChi3v(ROMol mol, bool force = false)
            => RDKFuncs.calcChi3v(mol, force);

        public static double CalcChi4n(ROMol mol, bool force = false)
            => RDKFuncs.calcChi4n(mol, force);

        public static double CalcChi4v(ROMol mol, bool force = false)
            => RDKFuncs.calcChi4v(mol, force);

        public static double CalcChiNn(ROMol mol, int n, bool force = false)
            => RDKFuncs.calcChiNn(mol, (uint)n, force);

        public static double CalcChiNv(ROMol mol, int n, bool force = false)
            => RDKFuncs.calcChiNv(mol, (uint)n, force);

        public static Double_Pair CalcCrippenDescriptors(ROMol mol, bool includeHs = true, bool force = false)
            => RDKFuncs.calcCrippenDescriptors(mol, includeHs, force);

        public static double CalcExactMolWt(ROMol mol, bool onlyHeavy = false)
            => RDKFuncs.calcExactMW(mol, onlyHeavy);

        public static double CalcFractionCSP3(ROMol mol)
            => RDKFuncs.calcFractionCSP3(mol);

        public static double CalcHallKierAlpha(ROMol mol, IReadOnlyList<double> atomContribs = null)
            => RDKFuncs.calcHallKierAlpha(mol, To_Double_Vect(atomContribs));

        public static double CalcKappa1(ROMol mol)
            => RDKFuncs.calcKappa1(mol);

        public static double CalcKappa2(ROMol mol)
            => RDKFuncs.calcKappa2(mol);

        public static double CalcKappa3(ROMol mol)
            => RDKFuncs.calcKappa3(mol);

        public static double CalcLabuteASA(ROMol mol, bool includeHs = true, bool force = false)
            => RDKFuncs.calcLabuteASA(mol, includeHs, force);

        public static string CalcMolFormula(ROMol mol, bool separateIsotopes = false, bool abbreviateHIsotopes = true)
            => RDKFuncs.calcMolFormula(mol, separateIsotopes, abbreviateHIsotopes);

        public static int CalcNumAliphaticCarbocycles(ROMol mol)
            => (int)RDKFuncs.calcNumAliphaticCarbocycles(mol);

        public static int CalcNumAliphaticHeterocycles(ROMol mol)
            => (int)RDKFuncs.calcNumAliphaticHeterocycles(mol);

        public static int CalcNumAliphaticRings(ROMol mol)
            => (int)RDKFuncs.calcNumAliphaticRings(mol);

        public static int CalcNumAmideBonds(ROMol mol)
            => (int)RDKFuncs.calcNumAmideBonds(mol);

        public static int CalcNumAromaticCarbocycles(ROMol mol)
            => (int)RDKFuncs.calcNumAromaticCarbocycles(mol);

        public static int CalcNumAromaticHeterocycles(ROMol mol)
            => (int)RDKFuncs.calcNumAromaticHeterocycles(mol);

        public static int CalcNumAromaticRings(ROMol mol)
            => (int)RDKFuncs.calcNumAromaticRings(mol);

        public static int CalcNumAtomStereoCenters(ROMol mol)
            => (int)RDKFuncs.numAtomStereoCenters(mol);

        public static int CalcNumBridgeheadAtoms(ROMol mol, IReadOnlyList<int> atoms = null)
            => (int)RDKFuncs.calcNumBridgeheadAtoms(mol, To_UInt_Vect(atoms));

        public static int CalcNumHBA(ROMol mol)
            => (int)RDKFuncs.calcNumHBA(mol);

        public static int CalcNumHBD(ROMol mol)
            => (int)RDKFuncs.calcNumHBD(mol);

        public static int CalcNumHeteroatoms(ROMol mol)
            => (int)RDKFuncs.calcNumHeteroatoms(mol);

        public static int CalcNumHeterocycles(ROMol mol)
            => (int)RDKFuncs.calcNumHeterocycles(mol);

        public static int CalcNumLipinskiHBA(ROMol mol)
            => (int)RDKFuncs.calcLipinskiHBA(mol);

        public static int CalcNumLipinskiHBD(ROMol mol)
            => (int)RDKFuncs.calcLipinskiHBD(mol);

        public static int CalcNumRings(ROMol mol)
            => (int)RDKFuncs.calcNumRings(mol);

        public static int CalcNumRotatableBonds(ROMol mol, bool strict)
            => (int)RDKFuncs.calcNumRotatableBonds(mol, strict);

        public static int CalcNumRotatableBonds(
            ROMol mol, 
            NumRotatableBondsOptions useStrictDefinition = NumRotatableBondsOptions.Default)
            => (int)RDKFuncs.calcNumRotatableBonds(mol, useStrictDefinition);

        public static int CalcNumSaturatedCarbocycles(ROMol mol)
            => (int)RDKFuncs.calcNumSaturatedCarbocycles(mol);

        public static int CalcNumSaturatedHeterocycles(ROMol mol)
            => (int)RDKFuncs.calcNumSaturatedHeterocycles(mol);

        public static int CalcNumSaturatedRings(ROMol mol)
            => (int)RDKFuncs.calcNumSaturatedRings(mol);

        public static int CalcNumSpiroAtoms(ROMol mol, IReadOnlyList<int> atoms = null)
            => (int)RDKFuncs.calcNumSpiroAtoms(mol, To_UInt_Vect(atoms));

        public static int CalcNumUnspecifiedAtomStereoCenters(ROMol mol)
            => (int)RDKFuncs.numUnspecifiedAtomStereoCenters(mol);

        public static double CalcPhi(ROMol mol)
            => RDKFuncs.calcPhi(mol);

        public static double CalcTPSA(ROMol mol, bool force = false, bool includeSandP = false)
            => RDKFuncs.calcTPSA(mol, force, includeSandP);

        public static Double_Vect CustomProp_VSA_(ROMol mol, string customPropName, IReadOnlyList<double> bins, bool force = false)
            => RDKFuncs.calcCustomProp_VSA(mol, customPropName, To_Double_Vect(bins), force);

        public static int GetAtomPairCode(int codeI, int codeJ, int dist, bool includeChirality)
            => (int)RDKFuncs.getAtomPairCode((uint)codeI, (uint)codeJ, (uint)dist, includeChirality);

        public static SparseIntVect32 GetAtomPairFingerprint(
            ROMol mol, 
            int minLength = 1, 
            int maxLength = 30, 
            IReadOnlyList<int> fromAtoms = null, 
            IReadOnlyList<int> ignoreAtoms = null, 
            IReadOnlyList<int> atomInvariants = null, 
            bool includeChirality = false, 
            bool use2D = true, 
            int confId = -1)
            => RDKFuncs.getAtomPairFingerprint(
                mol, 
                (uint)minLength, 
                (uint)maxLength, 
                To_UInt_Vect(fromAtoms), 
                To_UInt_Vect(ignoreAtoms), 
                To_UInt_Vect(atomInvariants), 
                includeChirality, 
                use2D, 
                confId);

        public static IList<int> GetConnectivityInvariants(ROMol mol, bool includeRingMembership)
        {
            var invars = new UInt_Vect((int)mol.getNumAtoms());
            RDKFuncs.getConnectivityInvariants(mol, invars, includeRingMembership);
            return invars.Cast<int>().ToList();
        }

        public static IList<int> GetFeatureInvariants(ROMol mol)
        {
            var invars = new UInt_Vect((int)mol.getNumAtoms());
            RDKFuncs.getFeatureInvariants(mol, invars);
            return invars.Cast<int>().ToList();
        }

        public static SparseIntVect32 GetHashedAtomPairFingerprint(
            ROMol mol, 
            int nBits = 2048, 
            int minLength = 1, 
            int maxLength = 30, 
            IReadOnlyList<int> fromAtoms = null,
            IReadOnlyList<int> ignoreAtoms = null,
            IReadOnlyList<int> atomInvariants = null, 
            bool includeChirality = false, 
            bool use2D = true, 
            int confId = -1)
            => RDKFuncs.getHashedAtomPairFingerprint(
                mol, 
                (uint)nBits, 
                (uint)minLength, 
                (uint)maxLength, 
                To_UInt_Vect(fromAtoms), 
                To_UInt_Vect(ignoreAtoms),
                To_UInt_Vect(atomInvariants), 
                includeChirality, 
                use2D, 
                confId);

        public static ExplicitBitVect GetHashedAtomPairFingerprintAsBitVect(
            ROMol mol, 
            int nBits = 2048, 
            int minLength = 1, 
            int maxLength = 30,
            IReadOnlyList<int> fromAtoms = null,
            IReadOnlyList<int> ignoreAtoms = null,
            IReadOnlyList<int> atomInvariants = null, 
            int nBitsPerEntry = 4, 
            bool includeChirality = false, 
            bool use2D = true, 
            int confId = -1)
            => RDKFuncs.getHashedAtomPairFingerprintAsBitVect(
                mol, 
                (uint)nBits, 
                (uint)minLength, 
                (uint)maxLength,
                To_UInt_Vect(fromAtoms),
                To_UInt_Vect(ignoreAtoms),
                To_UInt_Vect(atomInvariants), 
                (uint)nBitsPerEntry, 
                includeChirality, 
                use2D, 
                confId);

        public static SparseIntVect64 GetHashedTopologicalTorsionFingerprint(
            ROMol mol, 
            int nBits = 2048, 
            int targetSize = 4,
            IReadOnlyList<int> fromAtoms = null,
            IReadOnlyList<int> ignoreAtoms = null,
            IReadOnlyList<int> atomInvariants = null, 
            bool includeChirality = false)
            => RDKFuncs.getHashedTopologicalTorsionFingerprint(
                mol,
                (uint)nBits,
                (uint)targetSize,
                To_UInt_Vect(fromAtoms),
                To_UInt_Vect(ignoreAtoms),
                To_UInt_Vect(atomInvariants),
                includeChirality);

        public static ExplicitBitVect GetHashedTopologicalTorsionFingerprintAsBitVect(
            ROMol mol,
            int nBits = 2048, 
            int targetSize = 4,
            IReadOnlyList<int> fromAtoms = null,
            IReadOnlyList<int> ignoreAtoms = null,
            IReadOnlyList<int> atomInvariants = null, 
            int nBitsPerEntry = 4, 
            bool includeChirality = false)
            => RDKFuncs.getHashedTopologicalTorsionFingerprintAsBitVect(
                mol, 
                (uint)nBits, 
                (uint)targetSize,
                To_UInt_Vect(fromAtoms),
                To_UInt_Vect(ignoreAtoms),
                To_UInt_Vect(atomInvariants), 
                (uint)nBitsPerEntry,
                includeChirality);

        public static ExplicitBitVect GetMACCSKeysFingerprint(ROMol mol)
            => RDKFuncs.MACCSFingerprintMol(mol);

        public static SparseIntVectu32 GetMorganFingerprint(
            ROMol mol, int radius,
            IReadOnlyList<int> invariants = null,
            IReadOnlyList<int> fromAtoms = null, 
            bool useChirality = false, 
            bool useBondTypes = true, 
            bool onlyNonzeroInvariants = false, 
            bool useCounts = true, 
            BitInfoMap atomsSettingBits = null)
            => RDKFuncs.MorganFingerprintMol(
                mol, 
                (uint)radius, 
                To_UInt_Vect_0(invariants), 
                To_UInt_Vect_0(fromAtoms), 
                useChirality, 
                useBondTypes, 
                useCounts, 
                onlyNonzeroInvariants, 
                atomsSettingBits);

        public static ExplicitBitVect GetMorganFingerprintAsBitVect(
            ROMol mol, 
            int radius, 
            int nBits = 2048,
            IReadOnlyList<int> invariants = null,
            IReadOnlyList<int> fromAtoms = null, 
            bool useChirality = false, 
            bool useBondTypes = true, 
            bool onlyNonzeroInvariants = false, 
            BitInfoMap atomsSettingBits = null)
            => RDKFuncs.getMorganFingerprintAsBitVect(
                mol, 
                (uint)radius, 
                (uint)nBits,
                To_UInt_Vect_0(invariants),
                To_UInt_Vect_0(fromAtoms),
                useChirality, 
                useBondTypes, 
                onlyNonzeroInvariants, 
                atomsSettingBits);

        public static SparseIntVect64 GetTopologicalTorsionFingerprint(
            ROMol mol, 
            int targetSize = 4,
            IReadOnlyList<int> fromAtoms = null,
            IReadOnlyList<int> ignoreAtoms = null,
            IReadOnlyList<int> atomInvariants = null, 
            bool includeChirality = false)
            => RDKFuncs.getTopologicalTorsionFingerprint(
                mol,
                (uint)targetSize,
                To_UInt_Vect(fromAtoms),
                To_UInt_Vect(ignoreAtoms), 
                To_UInt_Vect(atomInvariants), 
                includeChirality);

        public static IList<int> MQNs_(ROMol mol, bool force = false)
            => RDKFuncs.calcMQNs(mol, force).Cast<int>().ToList();

        public static Double_Vect PEOE_VSA_(ROMol mol, IReadOnlyList<double> bins = null, bool force = false)
            => RDKFuncs.calcPEOE_VSA(mol, To_Double_Vect_0(bins), force);

        public static Double_Vect SMR_VSA_(ROMol mol, IReadOnlyList<double> bins = null, bool force = false)
            => RDKFuncs.calcSMR_VSA(mol, To_Double_Vect_0(bins), force);

        public static Double_Vect SlogP_VSA_(ROMol mol, IReadOnlyList<double> bins = null, bool force = false)
            => RDKFuncs.calcSlogP_VSA(mol, To_Double_Vect_0(bins), force);

        //
        // MolDescriptors3D
        //

        public static IReadOnlyList<double> CalcAUTOCORR3D(ROMol mol, int confId=-1, string customAtomPropName="")
        {
            var res = new Double_Vect(); 
            RDKFuncs.AUTOCORR3D(mol, res, confId, customAtomPropName);
            return res.ToList();
        }

        public static IReadOnlyList<IReadOnlyList<double>> CalcCoulombMat(ROMol mol, int confId=-1)
        {
            var res = new Double_Vect_Vect();
            RDKFuncs.CoulombMat(mol, res, confId);
            return res.ToList().Select(n => n.ToList()).ToList();
        }

        public static IReadOnlyList<double> CalcEEMcharges(ROMol mol, int confId = -1)
        {
            var res = new Double_Vect();
            RDKFuncs.EEM(mol, res, confId);
            return res.ToList();
        }

        public static double CalcEccentricity(ROMol mol, int confId=-1, bool useAtomicMasses=true, bool force=true)
            => RDKFuncs.eccentricity(mol, confId, useAtomicMasses, force);

        public static IReadOnlyList<double> CalcGETAWAY(ROMol mol, int confId = -1, uint precision = 2, string customAtomPropName = "")
        {
            var res = new Double_Vect();
            RDKFuncs.GETAWAY(mol, res, confId, precision, customAtomPropName);
            return res.ToList();
        }

        public static double CalcInertialShapeFactor(ROMol mol, int confId=-1, bool useAtomicMasses=true , bool force=true)
            => RDKFuncs.inertialShapeFactor(mol, confId, useAtomicMasses, force);

        public static IReadOnlyList<double> CalcMORSE(ROMol mol, int confId=-1, string customAtomPropName = "")
        {
            var res = new Double_Vect();
            RDKFuncs.MORSE(mol, res, confId, customAtomPropName);
            return res.ToList();
        }

        public static double CalcNPR1(ROMol mol, int confId = -1, bool useAtomicMasses=true, bool force=true)
            => RDKFuncs.NPR1(mol, confId, useAtomicMasses, force);

        public static double CalcNPR2(ROMol mol, int confId = -1, bool useAtomicMasses = true, bool force = true)
            => RDKFuncs.NPR2(mol, confId, useAtomicMasses, force);

        public static double CalcPBF(ROMol mol, int confId = -1)
            => RDKFuncs.PBF(mol, confId);

        public static double CalcPMI1(ROMol mol, int confId = -1, bool useAtomicMasses = true, bool force = true)
            => RDKFuncs.PMI1(mol, confId, useAtomicMasses, force);

        public static double CalcPMI2(ROMol mol, int confId = -1, bool useAtomicMasses = true, bool force = true)
            => RDKFuncs.PMI2(mol, confId, useAtomicMasses, force);

        public static double CalcPMI3(ROMol mol, int confId = -1, bool useAtomicMasses = true, bool force = true)
            => RDKFuncs.PMI3(mol, confId, useAtomicMasses, force);

        public static IReadOnlyList<double> CalcRDF(ROMol mol, int confId = -1,  string customAtomProperty="")
        {
            var res = new Double_Vect();
            RDKFuncs.RDF(mol, res, confId, customAtomProperty);
            return res.ToList();
        }

        public static double CalcRadiusOfGyration(ROMol mol, int confId = -1, bool useAtomicMasses = true, bool force = true)
            => RDKFuncs.radiusOfGyration(mol, confId, useAtomicMasses, force);

        public static double CalcSpherocityIndex(ROMol mol, int confId = -1, bool force = true)
             => RDKFuncs.spherocityIndex(mol, confId, force);


        public static IReadOnlyList<double> CalcWHIM(ROMol mol, int confId=-1, double th=0.001, string customAtomPropName="")
        {
            var res = new Double_Vect();
            RDKFuncs.WHIM(mol, res, confId, th, customAtomPropName);
            return res.ToList();
        }

        public static IReadOnlyList<double> GetAtomFeatures(ROMol mol, int atomid, bool addchiral =false)
        {
            var res = new Double_Vect();
            RDKFuncs.AtomFeatVect(mol, res, atomid, addchiral);
            return res.ToList();
        }

        public static int GetAtomPairAtomCode(Atom atom, int branchSubtract = 0, bool includeChirality = false)
            => (int)RDKFuncs.getAtomCode(atom, (uint)branchSubtract, includeChirality);

        public static IReadOnlyList<double> GetUSR(ROMol mol, int confId)
        {
            var res = new Double_Vect();
            RDKFuncs.USR(mol, res, confId);
            return res.ToList();
        }

        public static IReadOnlyList<double> GetUSRCAT(ROMol mol, IReadOnlyList<IReadOnlyList<int>> atomIds=null, int confId=-1)
        {
            var res = new Double_Vect();
            RDKFuncs.USRCAT(mol, res, To_UInt_Vect_Vect(atomIds), confId);
            return res.ToList();
        }

        public static IReadOnlyList<IReadOnlyList<double>> GetUSRDistributions(IReadOnlyList<Point3D> coords, IReadOnlyList<Point3D> points=null)
        {
            var res = new Double_Vect_Vect();
            RDKFuncs.calcUSRDistributions(new Point3D_Const_Vect(coords), res, points == null ? null : new Point3D_Val_Vect(points));
            return res.Select(n => n.ToList()).ToList();
        }

        public static IReadOnlyList<IReadOnlyList<double>> GetUSRDistributionsFromPoints(IReadOnlyList<Point3D> coords, IReadOnlyList<Point3D> points)
        {
            var res = new Double_Vect_Vect();
            RDKFuncs.calcUSRDistributionsFromPoints(new Point3D_Const_Vect(coords), points == null ? null : new Point3D_Val_Vect(points), res);
            return res.Select(n => n.ToList()).ToList();
        }

        public static IReadOnlyList<double> GetUSRFromDistributions(IReadOnlyList<IReadOnlyList<double>> dist)
        {
            var res = new Double_Vect();
            RDKFuncs.calcUSRFromDistributions(To_Double_Vect_Vect(dist), res);
            return res.ToList();
        }

        public static double GetUSRScore(IReadOnlyList<double> d1, IReadOnlyList<double> d2, IReadOnlyList<double> weights)
            => RDKFuncs.calcUSRScore(To_Double_Vect(d1), To_Double_Vect(d2), To_Double_Vect(weights));
    }
}
