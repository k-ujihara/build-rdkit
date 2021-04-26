using GraphMolWrap;
using System;

namespace RDKit
{
#pragma warning disable CA1032 // Implement standard exception constructors
#pragma warning disable CA2237 // Mark ISerializable types with serializable
    public class InchiReadWriteException : Exception
#pragma warning restore CA2237 // Mark ISerializable types with serializable
#pragma warning restore CA1032 // Implement standard exception constructors
    {
        public InchiReadWriteException(string inchi, string aux, string message)
            : base($"inchi={inchi}, aux={aux}, {message}")
        {
        }
    }

    public static partial class Chem
    {
        // 
        // rdkit.Chem.inchi module
        //

        public static (string inchi, string aux) MolToInchiAndAuxInfo(ROMol mol, string options = "", bool treatWarningAsError = false)
        {
            // TODO: logLevel
            var ex = new ExtraInchiReturnValues();
            var inchi = RDKFuncs.MolToInchi(mol, ex, options);
            if (treatWarningAsError && ex.returnCode != 0)
                throw new InchiReadWriteException(inchi, ex.auxInfoPtr, ex.messagePtr);
            return (inchi, ex.auxInfoPtr);
        }

        public static string MolToInchi(ROMol mol, string options = "", ExtraInchiReturnValues ex = null)
        {
            return RDKFuncs.MolToInchi(mol, ex ?? new ExtraInchiReturnValues(), options);
        }

        public static (string inchi, string aux) MolBlockToInchiAndAuxInfo(string molblock, string options = "", bool treatWarningAsError = false)
        {
            // TODO: logLevel
            var ex = new ExtraInchiReturnValues();
            var inchi = RDKFuncs.MolBlockToInchi(molblock, ex, options);
            if (treatWarningAsError && ex.returnCode != 0)
                throw new InchiReadWriteException(inchi, ex.auxInfoPtr, ex.messagePtr);
            return (inchi, ex.auxInfoPtr);
        }

        public static string MolBlockToInchi(string molblock, string options = "", ExtraInchiReturnValues ex = null)
        {
            return RDKFuncs.MolBlockToInchi(molblock, ex ?? new ExtraInchiReturnValues(), options);
        }

        public static RWMol MolFromInchi(string inchi, bool sanitize = true, bool removeHs = true, bool treatWarningAsError = false)
        {
            // TODO: logLevel
            var ex = new ExtraInchiReturnValues();
            var mol = RDKFuncs.InchiToMol(inchi, ex, sanitize, removeHs);
            if (treatWarningAsError && ex.returnCode != 0)
                throw new InchiReadWriteException(inchi, ex.auxInfoPtr, ex.messagePtr);
            return mol;
        }

        public static string InchiToInchiKey(string inchi)
        {
            return RDKFuncs.InchiToInchiKey(inchi);
        }

        public static RWMol InchiToMol(string inchi, bool sanitize = true, bool removeHs = true, ExtraInchiReturnValues ex = null)
        {
            return RDKFuncs.InchiToMol(inchi, ex ?? new ExtraInchiReturnValues(), sanitize, removeHs);
        }

        public static string MolToInchiKey(ROMol mol, string options = "")
        {
            return RDKFuncs.MolToInchiKey(mol, options);
        }
    }
}
