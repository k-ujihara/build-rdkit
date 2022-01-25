@pushd %~dp0
nmake -f Makefile.win PLATFORM=x64 clean
nmake -f Makefile.win PLATFORM=x86 clean
@popd
