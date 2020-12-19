using GraphMolWrap;
using System;
using System.IO;
using System.Text;

namespace RDKitCSharpTest
{
    class Program
    {
        static void ErrorHandle()
        {
            var invalid = RWMol.MolFromSmiles("dfep3js2g");
        }

        static void Demo()
        { 
            var toluene = RWMol.MolFromSmiles("Cc1ccccc1");            
            var mol1 = RWMol.MolFromMolFile(Path.Combine("Data", "input.mol"));
            var stringWithMolData = new StreamReader(Path.Combine("Data", "input.mol")).ReadToEnd();
            var mol2 = RWMol.MolFromMolBlock(stringWithMolData);

            using (var suppl = new SDMolSupplier(Path.Combine("Data", "5ht3ligs.sdf")))
            {
                while (!suppl.atEnd())
                {
                    var mol = suppl.next();
                    if (mol == null)
                        continue;
                    Console.WriteLine(mol.getAtoms().Count);

                    using (var maccs = RDKFuncs.MACCSFingerprintMol(mol))
                    {
                        Console.WriteLine(ToString(maccs));
                    }
                }
            }

            using (var gzsuppl = new ForwardSDMolSupplier(new gzstream("Data/actives_5ht3.sdf.gz")))
            {
                while (!gzsuppl.atEnd())
                {
                    var mol = gzsuppl.next();
                    if (mol == null)
                        continue;
                    Console.WriteLine(mol.getAtoms().Count);
                    using (var maccs = RDKFuncs.MACCSFingerprintMol(mol))
                    {
                        Console.WriteLine(ToString(maccs));
                    }
                }
            }
        }

        static string ToString(BitVect vector)
        {
            var sb = new StringBuilder();
            var n = vector.size();
            for (uint i = 0; i < n; i++)
                sb.Append(vector.getBit(i) ? '1' : '0');
            return sb.ToString();
        }

        static void CreateSomeObjects()
        {
            // ----- Object creation -----
            Console.WriteLine("Creating some objects:");

            ROMol m1 = RWMol.MolFromSmiles("c1ccccc1");
            Console.WriteLine(" mol: " + m1 + " " + m1.getNumAtoms());
            ROMol m2 = RWMol.MolFromSmiles("c1ccccn1");
            Console.WriteLine(" smi: " + m1 + " " + m1.MolToSmiles());
            Console.WriteLine(" smi2: " + m2 + " " + m2.MolToSmiles());

            ExplicitBitVect fp1 = RDKFuncs.LayeredFingerprintMol(m1);
            ExplicitBitVect fp2 = RDKFuncs.LayeredFingerprintMol(m2);

            Console.WriteLine(" sim: " + RDKFuncs.TanimotoSimilarityEBV(fp1, fp2));

            const string SMILES_benzene = "c1ccccc1";
            ROMol m3 = RWMol.MolFromSmiles(SMILES_benzene);
            uint nAtoms = m3.getNumAtoms(true);
            Console.WriteLine($"The number of atoms in {SMILES_benzene} is {nAtoms}.");
        }

        static void BulkMemoryLeakTest()
        {
            Console.WriteLine("Bulk memory leak test");
            for (uint i = 0; i < 10000; ++i)
            {
                ROMol m4 = RWMol.MolFromSmiles("Clc1cccc(N2CCN(CCC3CCC(CC3)NC(=O)c3cccs3)CC2)c1Cl");
                if ((i % 1000) == 0)
                    Console.WriteLine(" Done: " + i);
                m4.Dispose();
                //GC.Collect();
            }
        }

        static void MakePicture(string smiles, string filename)
        {
            int width = 200;
            int height = 200;

            RWMol mol = null;
            mol = RWMol.MolFromSmiles(smiles);
            if (mol == null)
                mol = RWMol.MolFromSmarts(smiles);
            if (mol == null)
                throw new Exception($"Cannot recognize: '{smiles}'");

            MolDraw2DSVG view = new MolDraw2DSVG(width, height);
            RDKFuncs.prepareMolForDrawing(mol);
            view.drawMolecule(mol);
            view.finishDrawing();

            using (var w = new StreamWriter(filename))
            {
                w.Write(view.getDrawingText());
                Console.WriteLine($"{filename} is drawn.");
            }
        }

        static void MakePictures()
        {
            MakePicture("c1ccccc1", "benzene.svg");
            MakePicture("Clc1cccc(N2CCN(CCC3CCC(CC3)NC(=O)c3cccs3)CC2)c1Cl", "mol.svg");
        }

        static void Main(string[] args)
        {
            ErrorHandle();
            Demo();
            CreateSomeObjects();
            BulkMemoryLeakTest();
            MakePictures();
            Console.WriteLine("Goodbye");
        }
    }
}
