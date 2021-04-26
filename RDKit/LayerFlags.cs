using System;

namespace RDKit
{
    [Flags]
    public enum LayerFlags
    {
        PureTopology = 0x1,
        BondOrder = 0x2,
        AtomTypes = 0x4,
        PresenceOfRings = 0x8,
        RingSize = 0x10,
        Aromaticity = 0x20,
    }
}
