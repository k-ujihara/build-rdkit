using GraphMolWrap;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        public static int AddAgentTemplate(this ChemicalReaction rxn, ROMol mol)
            => (int)rxn.addAgentTemplate(mol);

        public static int AddProductTemplate(this ChemicalReaction rxn, ROMol mol)
            => (int)rxn.addProductTemplate(mol);

        public static int AddReactantTemplate(this ChemicalReaction rxn, ROMol mol)
            => (int)rxn.addReactantTemplate(mol);

        public static void AddRecursiveQueriesToReaction(this ChemicalReaction rxn, StringMolMap queries = null, string propName = "molFileValue")
            => RDKFuncs.addRecursiveQueriesToReaction(rxn, queries ?? new StringMolMap(), propName);

        public static ROMol GetAgentTemplate(this ChemicalReaction rxn, int which)
            => rxn.getAgents()[which];

        public static ROMol_Vect GetAgents(this ChemicalReaction rxn)
            => rxn.getAgents();

        public static int GetNumAgentTemplates(this ChemicalReaction rxn)
            => (int)rxn.getNumAgentTemplates();

        public static int GetNumProductTemplates(this ChemicalReaction rxn)
            => (int)rxn.getNumProductTemplates();

        public static int GetNumReactantTemplates(this ChemicalReaction rxn)
            => (int)rxn.getNumReactantTemplates();

        public static ROMol GetProductTemplate(this ChemicalReaction rxn, int which)
            => rxn.getProducts()[which];

        public static ROMol_Vect GetProducts(this ChemicalReaction rxn)
            => rxn.getProducts();

        public static ROMol GetReactantTemplate(this ChemicalReaction rxn, int which)
            => rxn.getReactants()[which];

        public static ROMol_Vect GetReactants(this ChemicalReaction rxn)
            => rxn.getReactants();

        public static Int_Vect_Vect GetReactingAtoms(this ChemicalReaction rxn, bool mappedAtomsOnly = false)
            => RDKFuncs.getReactingAtoms(rxn, mappedAtomsOnly);

        public static bool IsMoleculeAgent(this ChemicalReaction rxn, ROMol mol)
            => RDKFuncs.isMoleculeAgentOfReaction(rxn, mol);

        public static bool IsMoleculeProduct(this ChemicalReaction rxn, ROMol mol)
            => RDKFuncs.isMoleculeProductOfReaction(rxn, mol);

        public static void Initialize(this ChemicalReaction rxn, bool silent = false)
            => rxn.initReactantMatchers(silent);

        public static bool IsMoleculeReactant(this ChemicalReaction rxn, ROMol mol)
            => RDKFuncs.isMoleculeReactantOfReaction(rxn, mol);

        public static bool IsInitialized(this ChemicalReaction rxn)
            => rxn.isInitialized();

        public static void RemoveAgentTemplates(this ChemicalReaction rxn, ROMol_Vect targetVector = null)
            => rxn.removeAgentTemplates(targetVector);

        public static void RemoveUnmappedProductTemplates(
            this ChemicalReaction rxn,
            double thresholdUnmappedAtoms = 0.2,
            bool moveToAgentTemplates = true,
            ROMol_Vect targetVector = null)
            => rxn.removeUnmappedProductTemplates(thresholdUnmappedAtoms, moveToAgentTemplates, targetVector);

        public static void RemoveUnmappedReactantTemplates(this ChemicalReaction rxn,
            double thresholdUnmappedAtoms = 0.2, bool moveToAgentTemplates = true, ROMol_Vect targetVector = null)
            => rxn.removeUnmappedReactantTemplates(thresholdUnmappedAtoms, moveToAgentTemplates, targetVector);

        public static ROMol_Vect_Vect RunReactant(this ChemicalReaction rxn, ROMol reactant, int reactantTemplateIdx = 1000)
            => rxn.runReactant(reactant, (uint)reactantTemplateIdx);

        public static ROMol_Vect_Vect RunReactants(this ChemicalReaction rxn, ROMol_Vect reactants, int numProducts = 1000)
            => rxn.runReactants(reactants, (uint)numProducts);

        public static Int_Vect ToBinary(this ChemicalReaction rxn)
            => rxn.ToBinary();

        public static Int_Pair Validate(this ChemicalReaction rxn, bool silent = false)
            => rxn.validateReaction(silent);
    }
}
