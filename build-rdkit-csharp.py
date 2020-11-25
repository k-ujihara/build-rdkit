# It is for rdkit-Release_2019.09.1

import os
import sys
import subprocess
import re
import shutil

swig_patch_enabled: bool = True


def replace_file_string(filename, pattern_replace):
    with open(filename, "r", encoding="utf-8") as file:
        filedata = file.read()
        for pattern, replace in pattern_replace:
            filedata = re.sub(
                pattern, replace, filedata, flags=re.MULTILINE | re.DOTALL
            )
    with open(filename, "w", encoding="utf-8") as file:
        file.write(filedata)


this_dir = os.environ["THISDIR"]
rdkit_dir = os.environ["RDKITDIR"]
zlib_dir = os.environ["ZLIBDIR"]
boost_dir = os.environ["BOOSTDIR"]
eigen_dir = os.environ["EIGENDIR"]
swig_dir = os.environ["SWIG_DIR"]
freetype_dir = os.environ["FREETYPEDIR"]
build_dir = os.environ["BUILDDIR"]
build_dir_for_csharp = os.environ["BUILDDIRCSHARP"]
rdkit_csharp_build_dir = os.path.join(rdkit_dir, build_dir_for_csharp)
build_platform = os.environ["BUILDPLATFORM"]
g_option_of_cmake = cmake_g = os.environ["CMAKEG"]
ms_build_platform = os.environ["MSBUILDPLATFORM"]
number_of_processors = os.environ["NUMBER_OF_PROCESSORS"]
boost_bin_dir = os.path.join(boost_dir, f"lib{build_platform}-msvc-14.1")
zlib_lib = os.path.join(os.path.join(zlib_dir, build_dir), "Release/zlib.lib")
rdkit_csharp_wrapper_dir = os.path.join(rdkit_dir, "Code/JavaWrappers/csharp_wrapper",)
rdkit_swig_csharp_dir = os.path.join(rdkit_csharp_wrapper_dir, "swig_csharp")

curr_dir = os.getcwd()
os.makedirs(rdkit_csharp_build_dir, exist_ok=True)
os.chdir(rdkit_csharp_build_dir)

if swig_patch_enabled:
    replace_file_string(
        os.path.join(rdkit_dir, "Code/JavaWrappers/csharp_wrapper/GraphMolCSharp.i",),
        [("boost::int32_t", "int32_t"), ("boost::uint32_t", "uint32_t")],
    )

cmd = (
    "cmake "
    + "-DRDK_BUILD_SWIG_WRAPPERS=ON "
    + "-DRDK_BUILD_SWIG_CSHARP_WRAPPER=ON "
    + "-DRDK_BUILD_SWIG_JAVA_WRAPPER=OFF "
    + "-DRDK_BUILD_PYTHON_WRAPPERS=OFF "
    + f"-DBOOST_ROOT={boost_dir} "
    + f"-DBOOST_INCLUDEDIR={boost_dir} "
    + f"-DBOOST_LIBRARYDIR={boost_bin_dir} "
    + f"-DZLIB_LIBRARY={zlib_lib} "
    + f"-DZLIB_INCLUDE_DIR={zlib_dir} "
    + f"-DEIGEN3_INCLUDE_DIR={eigen_dir} "
    + "-DRDK_INSTALL_INTREE=OFF "
    + "-DRDK_BUILD_CPP_TESTS=ON "
    + "-DRDK_BUILD_THREADSAFE_SSS=ON "
    + "-DRDK_BUILD_INCHI_SUPPORT=ON "
    + "-DRDK_BUILD_AVALON_SUPPORT=ON "
    + f'-G"{g_option_of_cmake}" '
    + ".."
)
cmd = cmd.replace("\\", "/")
print(cmd)
try:
    subprocess.check_call(cmd)
except subprocess.CalledProcessError as e:
    print(e)
    sys.exit(e.returncode)

cmd = (
    "MSBuild RDKit.sln /p:Configuration=Release,Platform="
    + ms_build_platform
    + " /maxcpucount"
)
print(cmd)
try:
    subprocess.check_call(cmd)
except subprocess.CalledProcessError as e:
    print(e)
    sys.exit(e.returncode)

dll_dest_dir = os.path.join(rdkit_csharp_wrapper_dir, build_platform)
os.makedirs(dll_dest_dir, exist_ok=True)
shutil.copy2(
    os.path.join(
        rdkit_csharp_build_dir, "Code/JavaWrappers/csharp_wrapper/Release/RDKFuncs.dll",
    ),
    dll_dest_dir,
)

# Customize the followings if required.

if swig_patch_enabled:
    replace_file_string(
        os.path.join(rdkit_swig_csharp_dir, "PropertyPickleOptions.cs"),
        [("BOOST_BINARY\\(\\s*([01]+)\\s*\\)", "0b\\1")],
    )
    replace_file_string(
        os.path.join(rdkit_swig_csharp_dir, "RDKFuncs.cs"),
        [
            (
                "public static double DiceSimilarity\\([^\\}]*\\.DiceSimilarity__SWIG_(12|13|14)\\([^\\}]*\\}",
                "",
            )
        ],
    )
replace_file_string(
    os.path.join(rdkit_swig_csharp_dir, "RDKFuncsPINVOKE.cs"),
    [("class RDKFuncsPINVOKE\\s*\\{", "partial class RDKFuncsPINVOKE {")],
)
replace_file_string(
    os.path.join(rdkit_swig_csharp_dir, "RDKFuncsPINVOKE.cs"),
    [
        (
            "static SWIGExceptionHelper\\(\\)\\s*\\{",
            "static SWIGExceptionHelper() { RDKFuncsPINVOKE.LoadDll();",
        )
    ],
)
shutil.copy2(
    os.path.join(this_dir, "csharp_wrapper/RDKFuncsPINVOKE_Loader.cs"),
    rdkit_swig_csharp_dir,
)
replace_file_string(
    os.path.join(rdkit_csharp_wrapper_dir, "RDKit2DotNet.csproj",),
    [
        (
            r"\<Content Include\=\"DKFuncs\.dll\"\>.*?\<\/Content\>\"",
            r'<Content Include="x64\\RDKFuncs.dll"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></Content>'  # NOQA
            r'<Content Include="x86\\RDKFuncs.dll"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></Content>',  # NOQA
        )
    ],
)
shutil.copy2(
    os.path.join(this_dir, "csharp_wrapper/RDKitCSharpTest.csproj"),
    os.path.join(rdkit_csharp_wrapper_dir, "RDKitCSharpTest"),
)
shutil.copy2(
    os.path.join(this_dir, "csharp_wrapper/RDKit2DotNet.sln",),
    rdkit_csharp_wrapper_dir,
)

print(
    'Solution file "'
    + os.path.join(rdkit_csharp_wrapper_dir, "RDKit2DotNet.sln")
    + '" is created. Modify issues like the followings if required.'
)
print("- Remove duplicated methods.")
print("- Rename miss named SWIGTYPE classes.")
print("- Add version infomation.")
print("- Signing if necessary.")

os.chdir(curr_dir)
