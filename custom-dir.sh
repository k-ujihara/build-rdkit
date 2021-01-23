export THIS_DIR=`dirname $0`
export MINOR_VERSION=4
export RDKIT_DIR=$THIS_DIR/rdkit-Release_2020_09_3

python3 ./build_rdkit_csharp.py --build_rdkit
