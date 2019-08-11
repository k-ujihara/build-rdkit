PUSHD %RDKITDIR%
MKDIR %BUILDDIRCSHARP%
CD %BUILDDIRCSHARP%

ECHO /* Fix 'GraphMolCSharp.i'. */   > replace_file.py
ECHO filename='%RDKITDIR:\=/%/Code/JavaWrappers/csharp_wrapper/GraphMolCSharp.i'  >> replace_file.py
ECHO with open(filename, 'r', encoding="utf-8") as file:                          >> replace_file.py
ECHO     filedata=file.read()                                                     >> replace_file.py
ECHO     filedata=filedata.replace('boost::int32_t', 'int32_t')                   >> replace_file.py
ECHO     filedata=filedata.replace('boost::uint32_t', 'uint32_t')                 >> replace_file.py
ECHO with open(filename, 'w', encoding="utf-8") as file:                          >> replace_file.py
ECHO     file.write(filedata)                                                     >> replace_file.py
python replace_file.py
DEL replace_file.py

@SET $EXE=cmake -DRDK_BUILD_SWIG_WRAPPERS=ON -DRDK_BUILD_SWIG_CSHARP_WRAPPER=ON -DRDK_BUILD_SWIG_JAVA_WRAPPER=OFF -DRDK_BUILD_PYTHON_WRAPPERS=OFF -DBOOST_ROOT="%BOOSTDIR%\stage\%BUILDPLATFORM%" -DZLIB_LIBRARY="%ZLIBDIR%\%BUILDDIR%\Release\zlib.lib" -DZLIB_INCLUDE_DIR="%ZLIBDIR%" -DEIGEN3_INCLUDE_DIR="%EIGENDIR%" -DRDK_INSTALL_INTREE=OFF -DCPACK_INSTALL_PREFIX=rdkit -DRDK_BUILD_THREADSAFE_SSS=ON -DRDK_BUILD_INCHI_SUPPORT=ON -DRDK_BUILD_AVALON_SUPPORT=ON -G"%CMAKEG%" ..
REM Replce backslash to slash because marparser recognize backslash as escape sequence.
@SET $EXE=%$EXE:\=/%
ECHO %$EXE%
%$EXE%
@SET $EXE=

MSBuild RDKit.sln /p:Configuration=Release,Platform=%MSBUILDPLATFORM% -maxcpucount:%NUMBER_OF_PROCESSORS%
MKDIR %RDKITDIR%\Code\JavaWrappers\csharp_wrapper\%BUILDPLATFORM%
COPY /Y %RDKITDIR%\%BUILDDIRCSHARP%\Code\JavaWrappers\csharp_wrapper\Release\RDKFuncs.dll %RDKITDIR%\Code\JavaWrappers\csharp_wrapper\%BUILDPLATFORM%

ECHO /* Replace BOOST_BINARY(n) to 0bn in 'PropertyPickleOptions.cs'. */    > replace_file.py
ECHO import re   >> replace_file.py
ECHO filename='%RDKITDIR:\=/%/Code/JavaWrappers/csharp_wrapper/swig_csharp/PropertyPickleOptions.cs'  >> replace_file.py
ECHO with open(filename, 'r', encoding="utf-8") as file:                          >> replace_file.py
ECHO     filedata=file.read()                                                     >> replace_file.py
ECHO     filedata=re.sub('BOOST_BINARY\\(\\s*([01]+)\\s*\\)', '0b\\1', filedata, flags=re.MULTILINE)  >> replace_file.py
ECHO with open(filename, 'w', encoding="utf-8") as file:                          >> replace_file.py
ECHO     file.write(filedata)                                                     >> replace_file.py
python replace_file.py
DEL replace_file.py

@ECHO Open '%RDKITDIR%\Code\JavaWrappers\csharp_wrapper\RDKit2DotNet.csproj' project and modify some issues like the followings manually.
@ECHO   - Remove RDKFuncs.dll from project, add %BUILDPLATFORM%\RDKFuncs.dll to the project, and set its build action to content.
@ECHO   - Remove duplicated methods.
@ECHO   - Rename miss named SWIGTYPE classes.
@ECHO   - Add partial directive to RDKFuncsPINVOKE class.
@ECHO   - Add class file '%THISDIR%\csharp_wrapper\RDKFuncsPINVOKE_Loader.cs'.
@ECHO   - Add version infomation
@ECHO   - Signing if requied.
PAUSE

POPD
