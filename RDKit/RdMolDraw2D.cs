// MIT License
// 
// Copyright (c) 2020-2021 Kazuya Ujihara
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

using GraphMolWrap;

namespace RDKit
{
    public static partial class Chem
    {
        public static partial class Draw
        {
            //
            // rdkit.Chem.Draw.rdMolDraw2D module
            //

            private static readonly ContourParams nullContourParams = new ContourParams();

            public static void ContourAndDrawGaussians(
                MolDraw2D drawer,
                Point2D_Vect p_locs,
                Double_Vect heights,
                Double_Vect widths,
                int nContours = 10,
                Double_Vect levels = null,
                ContourParams ps = null)
            {
                ps = ps ?? nullContourParams;
                RDKFuncs.ContourAndDrawGaussians(drawer, p_locs, heights, widths, (uint)nContours, levels, ps);
            }

            public static void ContourAndDrawGrid(
                MolDraw2D drawer, Double_Vect p_grid, Double_Vect xcoords, Double_Vect ycoords,
                int nContours = 10, Double_Vect levels = null, ContourParams ps = null)
            {
                ps = ps ?? nullContourParams;
                RDKFuncs.ContourAndDrawGrid(drawer, p_grid, xcoords, ycoords, (uint)nContours, levels, ps);
            }

            public static void PrepareAndDrawMolecule(MolDraw2D drawer, ROMol mol, string legend = "", Int_Vect highlight_atoms = null, Int_Vect highlight_bonds = null)
            {
                RDKFuncs.prepareAndDrawMolecule(drawer, mol, legend, highlight_atoms, highlight_bonds);
            }

            public static void PrepareMolForDrawing(RWMol mol, bool kekulize = true, bool addChiralHs = true, bool wedgeBonds = true, bool forceCoords = false)
            {
                RDKFuncs.prepareMolForDrawing(mol, kekulize, addChiralHs, wedgeBonds, forceCoords);
            }
        }
    }
}
