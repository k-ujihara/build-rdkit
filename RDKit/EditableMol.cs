using GraphMolWrap;
using System;

namespace RDKit
{
    public class EditableMol : IDisposable
    {
        private RWMol dp_mol;
        private bool disposedValue;

        public EditableMol(ROMol mol)
        {
            this.dp_mol = new RWMol(mol);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (!disposedValue)
            {
                if (disposing)
                {
                    this.dp_mol.Dispose();
                }

                disposedValue = true;
            }
        }

        public void Dispose()
        {
            // Do not change this code. Put cleanup code in 'Dispose(bool disposing)' method
            Dispose(disposing: true);
            GC.SuppressFinalize(this);
        }

        public void RemoveAtom(int idx) 
            => dp_mol.removeAtom((uint)idx);

        public void RemoveBond(int idx1, int idx2) 
            => dp_mol.removeBond((uint)idx1, (uint)idx2);

        public int AddBond(int begAtomIdx, int endAtomIdx, Bond.BondType order = Bond.BondType.UNSPECIFIED)
            => (int)dp_mol.addBond((uint)begAtomIdx, (uint)endAtomIdx, order);

        public int AddAtom(Atom atom)
            => (int)dp_mol.addAtom(atom, true);

        public void ReplaceAtom(int idx, Atom atom, bool updateLabels = false, bool preserveProps = false)
            => dp_mol.replaceAtom((uint)idx, atom, updateLabels, preserveProps);

        public void ReplaceBond(int idx, Bond bond, bool preserveProps = false)
            => dp_mol.replaceBond((uint)idx, bond, preserveProps);

        public void BeginBatchEdit()
            => dp_mol.beginBatchEdit();

        public void RollbackBatchEdit()
            => dp_mol.rollbackBatchEdit();

        public void CommitBatchEdit()
            => dp_mol.commitBatchEdit();

        public ROMol GetMol()
            => new ROMol(dp_mol);
    }
}
