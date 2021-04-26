using System;

namespace RDKit
{
    [Flags]
    public enum PDBFlavors
    {
        /// <summary>Write MODEL/ENDMDL lines around each record</summary>
        WriteMODEL = 1,
        /// <summary>Don't write any CONECT records</summary>
        DontWriteCONECT = 2,
        /// <summary>Write CONECT records in both directions</summary>
        WriteCONECTBoth = 4,
        /// <summary>Don't use multiple CONECTs to encode bond order</summary>
        DontUseMultipleCONECT = 8,
        /// <summary>Write MASTER record</summary>
        WriteMASTER = 16,
        /// <summary>Write TER record</summary>
        WriteTER = 32,
    }
}
