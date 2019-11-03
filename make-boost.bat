@pushd %BOOSTDIR%
@call bootstrap.bat
@setlocal
@set $EXE=b2 -sZLIB_SOURCE="%ZLIBDIR%" -sZLIB_INCLUDE="%ZLIBDIR%" -sZLIB_LIBPATH="%ZLIBDIR%\%BUILDDIR%\Release" -sZLIB_BINARY="%ZLIBDIR%\%BUILDDIR%\Release\zlib.lib" architecture=x86 address-model=%ADDRESSMODEL% threading=multi runtime-link=shared --build-type=minimal link=shared --stagedir=stage/%BUILDPLATFORM% stage -j %NUMBER_OF_PROCESSORS%
%$EXE%
@set $EXE=
@endlocal
@popd
