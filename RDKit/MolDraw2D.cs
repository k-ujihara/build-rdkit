using GraphMolWrap;
using System;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        //
        // MolDraw2D
        // 

        public static void ClearDrawing(this MolDraw2D view)
            => view.clearDrawing();

        public static void DrawArrow(
            this MolDraw2D view, Point2D cds1, Point2D cds2,
            bool asPolygon = false, double frac = 0.05, double angle = 0.5235987755982988)
            => view.drawArrow(cds1, cds2, asPolygon, frac, angle);
        public static void DrawAttachmentLine(
            this MolDraw2D view, Point2D cds1, Point2D cds2, DrawColour col,
            double len = 1.0, int nSegments = 16)
            => view.drawAttachmentLine(cds1, cds2, col, len, (uint)nSegments);
        public static void DrawEllipse(this MolDraw2D view, Point2D cds1, Point2D cds2)
            => view.drawEllipse(cds1, cds2);

        public static void DrawLine(this MolDraw2D view, Point2D cds1, Point2D cds2)
            => view.drawLine(cds1, cds2);

        public static void DrawMolecule(this MolDraw2D view, ROMol mol, Int_Vect highlight_atoms = null, Int_Vect highlight_bonds = null, string legend = "")
            => view.drawMolecule(mol, legend, highlight_atoms, highlight_bonds);

        public static void DrawMoleculeWithHighlights(this MolDraw2D view, ROMol mol, string legend, SWIGTYPE_p_std__mapT_int_std__vectorT_RDKit__DrawColour_t_std__lessT_int_t_t highlight_atom_map, SWIGTYPE_p_std__mapT_int_std__vectorT_RDKit__DrawColour_t_std__lessT_int_t_t highlight_bond_map, Int_Double_Map highlight_radii, Int_Int_Map highlight_linewidth_multipliers, int confId = -1)
            => view.drawMoleculeWithHighlights(mol, legend, highlight_atom_map, highlight_bond_map, highlight_radii, highlight_linewidth_multipliers, confId);

        public static void DrawMolecules(this MolDraw2D view, ROMol_Ptr_Vect mols, Int_Vect_Vect highlight_atoms = null, Int_Vect_Vect highlight_bonds = null, Str_Vect legends = null)
            => view.drawMolecules(mols, legends, highlight_atoms, highlight_bonds);

        public static void DrawPolygon(this MolDraw2D view, SWIGTYPE_p_std__vectorT_RDGeom__Point2D_t cds)
            => view.drawPolygon(cds);

        public static void DrawReaction(this MolDraw2D view, ChemicalReaction rxn, bool highlightByReactant = false, SWIGTYPE_p_std__vectorT_RDKit__DrawColour_t highlightColorsReactants = null, Int_Vect confIds = null)
            => view.drawReaction(rxn, highlightByReactant, highlightColorsReactants, confIds);

        public static void DrawRect(this MolDraw2D view, Point2D cds1, Point2D cds2)
        => view.drawRect(cds1, cds2);

        public static void DrawString(this MolDraw2D view, string str, Point2D cds, TextAlignType align)
            => view.drawString(str, cds, align);

        public static void DrawString(this MolDraw2D view, string str, Point2D cds)
            => view.drawString(str, cds);

        public static void DrawTriangle(this MolDraw2D view, Point2D cds1, Point2D cds2, Point2D cds3)
            => view.drawTriangle(cds1, cds2, cds3);

        public static void DrawWavyLine(this MolDraw2D view, Point2D cds1, Point2D cds2, DrawColour col1, DrawColour col2, int nSegments = 16, double vertOffset = 0.05)
            => view.drawWavyLine(cds1, cds2, col1, col2, (uint)nSegments, vertOffset);

        public static bool FillPolys(this MolDraw2D view)
            => view.fillPolys();

        public static double FontSize(this MolDraw2D view)
            => view.fontSize();

        public static Point2D GetDrawCoords(this MolDraw2D view, Point2D mol_cds)
            => view.getDrawCoords(mol_cds);

        public static Point2D GetDrawCoords(this MolDraw2D view, int at_num)
            => view.getDrawCoords(at_num);

        public static int Height(this MolDraw2D view)
        => view.height();

        public static int LineWidth(this MolDraw2D view)
            => view.lineWidth();

        public static Point2D Offset(this MolDraw2D view)
            => view.offset();

        public static void SetColour(this MolDraw2D view, DrawColour col)
        => view.setColour(col);

        public static void SetDrawOptions(MolDraw2D view, MolDrawOptions opts)
            => view.setDrawOptions(opts);

        public static void SetFillPolys(this MolDraw2D view, bool val)
            => view.setFillPolys(val);

        public static void SetFontSize(this MolDraw2D view, double new_size)
            => view.setFontSize(new_size);

        public static void SetLineWidth(this MolDraw2D view, int width)
            => view.setLineWidth(width);

        public static void SetOffset(this MolDraw2D view, int x, int y)
        => view.setOffset(x, y);
        public static void SetScale(this MolDraw2D view, int width, int height, Point2D minv, Point2D maxv)
            => view.setScale(width, height, minv, maxv);

        public static void SetScale(this MolDraw2D view, int width, int height, Point2D minv, Point2D maxv, ROMol mol)
            => view.setScale(width, height, minv, maxv, mol);

        public static int Width(this MolDraw2D view)
            => view.width();

        public static MolDrawOptions DrawOptions(this MolDraw2D view)
            => view.drawOptions();

        public static void FinishDrawing(this MolDraw2D view)
        {
            // abstract
            switch (view)
            {
                case MolDraw2DSVG d2d:
                    d2d.FinishDrawing();
                    break;
                case MolDraw2DCairo d2d:
                    d2d.FinishDrawing();
                    break;
                default:
                    throw new NotImplementedException();
            }
        }

        //
        // MolDraw2DCairo
        //

        public static void FinishDrawing(this MolDraw2DCairo view)
            => view.finishDrawing();

        public static string GetDrawingText(this MolDraw2DCairo view)
            => view.getDrawingText();

        public static void WriteDrawingText(this MolDraw2DCairo view, string fName)
        {
            view.writeDrawingText(fName);
        }

        //
        // MolDraw2DSVG
        //

        public static void AddMoleculeMetadata(this MolDraw2DSVG view, ROMol mol, int confId = -1)
        {
            view.addMoleculeMetadata(mol, confId);
        }

        public static void FinishDrawing(this MolDraw2DSVG view)
            => view.finishDrawing();

        public static string GetDrawingText(this MolDraw2DSVG view)
            => view.getDrawingText();

        public static void TagAtoms(this MolDraw2DSVG view, ROMol mol, double radius = 0.2, String_String_Map events = null)
        {
            view.tagAtoms(mol, radius, events);
        }
    }
}
