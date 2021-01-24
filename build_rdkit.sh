set -eu
export THIS_DIR=$(cd $(dirname $0); pwd)
export MINOR_VERSION=4
export RDKIT_DIR=$THIS_DIR/rdkit-Release_2020_09_3

python3 $THIS_DIR/build_rdkit_csharp.py --build_rdkit
