using GraphMolWrap;
using System;
using System.IO;
using System.Text;

namespace RDKit2DotNet.Example
{
    class Program
    {
        static void Main(string[] args)
        {
            Test();
            Demo();
        }

        static void Demo()
        { 
            var toluene = RWMol.MolFromSmiles("Cc1ccccc1");
            var mol1 = RWMol.MolFromMolFile("Data/input.mol");
            var stringWithMolData = new StreamReader("Data/input.mol").ReadToEnd();
            var mol2 = RWMol.MolFromMolBlock(stringWithMolData);

            using (var suppl = new SDMolSupplier("Data/5ht3ligs.sdf"))
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

        static void Test()
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

            //rxnTest();
            //smiTest();
            //morganTest();

            ROMol m3 = RWMol.MolFromSmiles("c1ccccc1");
            uint nAtoms = m3.getNumAtoms(true);

            Console.WriteLine("Bulk memory leak test");
            for (uint i = 0; i < 10000; ++i)
            {
                using (ROMol m4 = RWMol.MolFromSmiles("Clc1cccc(N2CCN(CCC3CCC(CC3)NC(=O)c3cccs3)CC2)c1Cl"))
                {
                    if ((i % 1000) == 0)
                        Console.WriteLine(" Done: " + i);
                }
            }

            Console.WriteLine("Goodbye");
        }
    }
}
