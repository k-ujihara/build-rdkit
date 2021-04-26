using GraphMolWrap;
using System.Collections.Generic;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        public static Point3D GetAtomPosition(this Conformer conformer, int atomIdx)
            => conformer.getAtomPos((uint)atomIdx);

        public static int GetId(this Conformer conformer)
            => (int)conformer.getId();

        public static int GetNumAtoms(this Conformer conformer)
            => (int)conformer.getNumAtoms();

        public static ROMol GetOwningMol(this Conformer conformer)
            => conformer.getOwningMol();

        public static IEnumerable<Point3D> GetPositions(this Conformer conformer)
        {
            var n = conformer.GetNumAtoms();
            for (var i = 0; i < n; i++)
            {
                yield return conformer.GetAtomPosition(i);
            }
            yield break;
        }

        public static bool HasOwningMol(this Conformer conformer)
            => conformer.hasOwningMol();

        public static bool Is3D(this Conformer conformer)
            => conformer.is3D();

        public static void Set3D(this Conformer conformer, bool v)
            => conformer.set3D(v);

        public static void SetAtomPosition(this Conformer conformer, int atomId, Point3D position)
            => conformer.setAtomPos((uint)atomId, position);

        public static void SetId(this Conformer conformer, int id)
            => conformer.setId((uint)id);
    }
}
