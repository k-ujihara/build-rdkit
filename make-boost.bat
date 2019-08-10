pushd %BOOSTDIR%
CALL bootstrap.bat
@SET $EXE=b2 -sZLIB_SOURCE="%ZLIBDIR%" -sZLIB_INCLUDE="%ZLIBDIR%" -sZLIB_LIBPATH="%ZLIBDIR%\%BUILDDIR%\Release" -sZLIB_BINARY="%ZLIBDIR%\%BUILDDIR%\Release\zlib.lib" architecture=x86 address-model=%MODEL% threading=multi runtime-link=shared --build-type=minimal link=shared --stagedir=stage/%MSBUILDPLATFORM% stage -j 8
ECHO %$EXE%
%$EXE%
@SET %$EXE%=
popd
