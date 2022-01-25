swig -version | grep "SWIG Version 3\." > /dev/null
if [ "$?" != "0" ] ; then
    echo SWIG version should be 3.0.
    exit 1
fi

python --version | grep -E "Python 3\.(8|9|10)\." > /dev/null
if [ "$?" != "0" ] ; then
    echo Python version is 3.8, 3.9, or 3.10.
    exit 1
fi

# Native files are generated in $(RDKIT_DIR)/Code/JavaWrappers/csharp_wrapper/linux/.
make -f Makefile.linux rdkit_native PLATFORM=x64
if [ "$?" != "0" ] ; then
    exit 1
fi
