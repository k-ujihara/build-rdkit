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
using System.Collections.Generic;
using System.Linq;

namespace RDKit
{
    public static partial class GraphMolWrapTools
    {
        public static int Count(this BitVect bv)
            => (int)bv.size();

        public static void ClearBits(this BitVect bv)
            => bv.clearBits();

        public static bool GetBit(this BitVect bv, int which)
            => bv.getBit((uint)which);

        public static bool SetBit(this BitVect bv, int which)
            => bv.setBit((uint)which);

        public static bool UnsetBit(this BitVect bv, int which)
            => bv.unsetBit((uint)which);

        public static int GetNumBits(this BitVect bv)
            => (int)bv.getNumBits();

        public static int GetNumOffBits(this BitVect bv)
            => (int)bv.getNumOffBits();

        public static int GetNumOnBits(this BitVect bv)
            => (int)bv.getNumOnBits();

        public static void GetOnBits(this BitVect bv, Int_Vect v)
            => bv.getOnBits(v);

        public static int Count(this SparseIntVect32 v)
            => (int)v.size();

        public static Match_Vect GetNonzero(this SparseIntVect32 v)
            => v.getNonzero();

        public static int Count(this SparseIntVectu32 v)
            => (int)v.size();

        public static UInt_Pair_Vect GetNonzero(this SparseIntVectu32 v)
            => v.getNonzero();

        public static int Count(this SparseIntVect64 v)
            => (int)v.size();

        public static Long_Pair_Vect GetNonzero(this SparseIntVect64 v)
            => v.getNonzero();

        internal static UInt_Vect To_UInt_Vect(IEnumerable<int> ints)
            => ints == null ? null : new UInt_Vect(ints);

        internal static UInt_Vect To_UInt_Vect_0(IEnumerable<int> ints)
            => ints == null ? new UInt_Vect(0) : new UInt_Vect(ints);

        internal static Double_Vect To_Double_Vect(IEnumerable<double> values)
            => values == null ? null : new Double_Vect(values);

        internal static Double_Vect To_Double_Vect_0(IEnumerable<double> values)
            => values == null ? new Double_Vect(0) : new Double_Vect(values);

        internal static UInt_Vect_Vect To_UInt_Vect_Vect(IEnumerable<IEnumerable<int>> intss)
            => intss == null ? null : new UInt_Vect_Vect(intss.Select(n => To_UInt_Vect(n)));

        internal static Double_Vect_Vect To_Double_Vect_Vect(IEnumerable<IEnumerable<double>> valuess)
            => valuess == null ? null : new Double_Vect_Vect(valuess.Select(n =>To_Double_Vect(n)));
    }
}
