using GraphMolWrap;
using System;

namespace RDKit
{
    public static partial class DataStructs
    {
        /// <summary>
        /// Calculated similarity between two fingerprints,
        /// handles any folding that may need to be done to ensure that they are compatible
        /// </summary>
        /// <param name="fp1"></param>
        /// <param name="fp2"></param>
        /// <param name="metric">Default is <see cref="TanimotoSimilarity(ExplicitBitVect, ExplicitBitVect)"/></param>
        /// <returns>The calculated similarity</returns>
        public static double FingerprintSimilarity(ExplicitBitVect fp1, ExplicitBitVect fp2, Func<ExplicitBitVect, ExplicitBitVect, double> metric = null)
        {
            metric = metric ?? TanimotoSimilarity;
            var sz1 = fp1.GetNumBits();
            var sz2 = fp2.GetNumBits();
            if (sz1 < sz2)
            {
                fp2 = RDKFuncs.FoldFingerprint(fp2, (uint)(sz2 / sz1));
            }
            else if (sz2 < sz1)
            {
                fp1 = RDKFuncs.FoldFingerprint(fp1, (uint)(sz1 / sz2));
            }
            return metric(fp1, fp2);
        }

        public static ExplicitBitVect FoldToTargetDensity(ExplicitBitVect fp, double density = 0.3, int minLength = 64)
        {
            while (fp.GetNumOnBits() / fp.Count() > density && fp.Count() / 2 > minLength)
                fp = RDKFuncs.FoldFingerprint(fp, 2);
            return fp;
        }
    }
}
