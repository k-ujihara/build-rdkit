
using GraphMolWrap;

namespace RDKit
{
    public static partial class DataStructs
    {
        public static double AllBitSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.AllBitSimilarity(bv1, bv2);
        public static double AsymmetricSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.AsymmetricSimilarity(bv1, bv2);
        public static double BraunBlanquetSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.BraunBlanquetSimilarity(bv1, bv2);
        public static double CosineSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.CosineSimilarity(bv1, bv2);
        public static double DiceSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.DiceSimilarity(bv1, bv2);
        public static double DiceSimilarity(SparseIntVect32 v1, SparseIntVect32 v2, bool returnDistance = false, double bounds = 0)
            => RDKFuncs.DiceSimilarity(v1, v2, returnDistance, bounds);
        public static double DiceSimilarity(SparseIntVectu32 v1, SparseIntVectu32 v2, bool returnDistance = false, double bounds = 0)
            => RDKFuncs.DiceSimilarity(v1, v2, returnDistance, bounds);
        public static double DiceSimilarity(SparseIntVect64 v1, SparseIntVect64 v2, bool returnDistance = false, double bounds = 0)
            => RDKFuncs.DiceSimilarity(v1, v2, returnDistance, bounds);
        public static double KulczynskiSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.KulczynskiSimilarity(bv1, bv2);
        public static double McConnaugheySimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.McConnaugheySimilarity(bv1, bv2);
        public static double OnBitSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.OnBitSimilarity(bv1, bv2);
        public static double RusselSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.RusselSimilarity(bv1, bv2);
        public static double SokalSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.SokalSimilarity(bv1, bv2);
        public static double TanimotoSimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2)
            => RDKFuncs.TanimotoSimilarityEBV(bv1, bv2);
        public static double TanimotoSimilarity(SparseIntVect32 v1, SparseIntVect32 v2, bool returnDistance = false, double bounds = 0)
            => RDKFuncs.TanimotoSimilaritySIVi32(v1, v2, returnDistance, bounds);
        public static double TanimotoSimilarity(SparseIntVect64 v1, SparseIntVect64 v2, bool returnDistance = false, double bounds = 0)
            => RDKFuncs.TanimotoSimilaritySIVi64(v1, v2, returnDistance, bounds);
        public static double TanimotoSimilarity(SparseIntVectu32 v1, SparseIntVectu32 v2, bool returnDistance = false, double bounds = 0)
            => RDKFuncs.TanimotoSimilaritySIVu32(v1, v2, returnDistance, bounds);
        public static double TverskySimilarity(ExplicitBitVect bv1, ExplicitBitVect bv2, double a, double b)
            => RDKFuncs.TverskySimilarity(bv1, bv2, a, b);
        public static double TverskySimilarity(SparseIntVect32 v1, SparseIntVect32 v2, double a, double b, bool returnDistance = false, double bounds = 0)
            => RDKFuncs.TverskySimilarity(v1, v2, a, b, returnDistance, bounds);
        public static double TverskySimilarity(SparseIntVectu32 v1, SparseIntVectu32 v2, double a, double b, bool returnDistance = false, double bounds = 0)
            => RDKFuncs.TverskySimilarity(v1, v2, a, b, returnDistance, bounds);
        public static double TverskySimilarity(SparseIntVect64 v1, SparseIntVect64 v2, double a, double b, bool returnDistance = false, double bounds = 0)
            => RDKFuncs.TverskySimilarity(v1, v2, a, b, returnDistance, bounds);
    }
}

