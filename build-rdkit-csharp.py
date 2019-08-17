# It is for rdkit-Release_2019_03_3

import os
import subprocess
import re
import subprocess
import shutil
import glob

def replace_file_string(filename, pattern_replace):
    with open(filename, 'r', encoding="utf-8") as file:
        filedata = file.read()
        for pattern, replace in pattern_replace:
            filedata = re.sub(pattern, replace, filedata, flags=re.MULTILINE | re.DOTALL)
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(filedata)

this_dir = os.environ['THISDIR']
rdkit_dir = os.environ['RDKITDIR']
zlib_dir = os.environ['ZLIBDIR']
boost_dir = os.environ['BOOSTDIR']
eigen_dir = os.environ['EIGENDIR']
build_dir = os.environ['BUILDDIR']
build_dir_for_csharp = os.environ['BUILDDIRCSHARP']
rdkit_csharp_build_dir = os.path.join(rdkit_dir, build_dir_for_csharp)
build_platform = os.environ['BUILDPLATFORM']
g_option_of_cmake = cmake_g = os.environ['CMAKEG']
ms_build_platform = os.environ['MSBUILDPLATFORM']
number_of_processors = os.environ['NUMBER_OF_PROCESSORS']
boost_bin_dir = os.path.join(os.path.join(boost_dir, 'stage'), build_platform)
zlib_lib = os.path.join(os.path.join(zlib_dir, build_dir), 'Release/zlib.lib')
rdkit_csharp_wrapper_dir = os.path.join(rdkit_dir, 'Code/JavaWrappers/csharp_wrapper')
rdkit_swig_csharp_dir = os.path.join(rdkit_csharp_wrapper_dir, 'swig_csharp')

curr_dir = os.getcwd()
os.makedirs(rdkit_csharp_build_dir, exist_ok = True)
os.chdir(rdkit_csharp_build_dir)

replace_file_string(os.path.join(rdkit_dir, 'Code/JavaWrappers/csharp_wrapper/GraphMolCSharp.i'), \
    [ ('boost::int32_t', 'int32_t'), \
      ('boost::uint32_t', 'uint32_t')])

cmd = 'cmake ' \
    '-DRDK_BUILD_SWIG_WRAPPERS=ON ' + \
    '-DRDK_BUILD_SWIG_CSHARP_WRAPPER=ON ' + \
    '-DRDK_BUILD_SWIG_JAVA_WRAPPER=OFF ' + \
    '-DRDK_BUILD_PYTHON_WRAPPERS=OFF ' + \
    '-DBOOST_ROOT="' + boost_bin_dir + '" ' + \
    '-DZLIB_LIBRARY="' + zlib_lib + '" ' + \
    '-DZLIB_INCLUDE_DIR="' + zlib_dir + '" ' + \
    '-DEIGEN3_INCLUDE_DIR="' + eigen_dir + '" ' + \
    '-DRDK_INSTALL_INTREE=OFF ' + \
    '-DRDK_BUILD_CPP_TESTS=OFF ' + \
    '-DRDK_BUILD_THREADSAFE_SSS=ON ' + \
    '-DRDK_BUILD_INCHI_SUPPORT=ON ' + \
    '-DRDK_BUILD_AVALON_SUPPORT=ON ' + \
    '-G"' + g_option_of_cmake + '" ' + \
    '..'
cmd = cmd.replace('\\', '/')
subprocess.check_call(cmd)

cmd = 'MSBuild RDKit.sln /p:Configuration=Release,Platform=' + ms_build_platform + ' -maxcpucount:' + number_of_processors
subprocess.check_call(cmd)

dll_dest_dir = os.path.join(rdkit_csharp_wrapper_dir, build_platform)
os.makedirs(dll_dest_dir, exist_ok = True)
shutil.copy2(os.path.join(rdkit_csharp_build_dir, 'Code/JavaWrappers/csharp_wrapper/Release/RDKFuncs.dll'), dll_dest_dir)

# Customize the followings if required.

replace_file_string(os.path.join(rdkit_swig_csharp_dir, 'PropertyPickleOptions.cs'), [('BOOST_BINARY\\(\\s*([01]+)\\s*\\)', '0b\\1')])
replace_file_string(os.path.join(rdkit_swig_csharp_dir, 'RDKFuncs.cs'), [('public static double DiceSimilarity\\([^\\}]*\\.DiceSimilarity__SWIG_(12|13|14)\\([^\\}]*\\}', '')])
replace_file_string(os.path.join(rdkit_swig_csharp_dir, 'RDKFuncsPINVOKE.cs'), [('class RDKFuncsPINVOKE\\s*\\{', 'partial class RDKFuncsPINVOKE {')])
replace_file_string(os.path.join(rdkit_swig_csharp_dir, 'RDKFuncsPINVOKE.cs'), [('static SWIGExceptionHelper\\(\\)\\s*\\{', 'static SWIGExceptionHelper() { RDKFuncsPINVOKE.LoadDll();')])
shutil.copy2(os.path.join(this_dir, 'csharp_wrapper/RDKFuncsPINVOKE_Loader.cs'), rdkit_swig_csharp_dir)
replace_file_string(os.path.join(rdkit_csharp_wrapper_dir, 'RDKit2DotNet.csproj'), \
    [('\\<Content Include\\=\\"RDKFuncs\\.dll\\"\\>.*?\\<\\/Content\\>', 
        '<Content Include="x64\RDKFuncs.dll"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></Content>' \
        '<Content Include="x86\RDKFuncs.dll"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></Content>')])
shutil.copy2(os.path.join(this_dir, 'csharp_wrapper/RDKitCSharpTest.csproj'), os.path.join(rdkit_csharp_wrapper_dir, 'RDKitCSharpTest'))
shutil.copy2(os.path.join(this_dir, 'csharp_wrapper/RDKit2DotNet.sln'), rdkit_csharp_wrapper_dir)

print('Open "' + os.path.join(rdkit_csharp_wrapper_dir, 'RDKit2DotNet.sln') + '" solution and modify some issues including the followings manually if required.')
print('- Remove duplicated methods.')
print('- Rename miss named SWIGTYPE classes.')
print('- Add version infomation.')
print('- Signing if required.')

os.chdir(curr_dir)
