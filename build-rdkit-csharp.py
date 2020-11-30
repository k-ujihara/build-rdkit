# It is for rdkit-Release_2019.09.1

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
import pathlib
from typing import Optional, Mapping, List, Dict
import glob


here = Path(__file__).parent.resolve()

cpu_models = ["x86", "x64"]
project_name = "RDKit.DotNetWrap"
swig_patch_enabled: bool = True


def get_path_from_env(dir: str) -> Optional[Path]:
    if dir not in os.environ:
        return None
    return Path(os.environ[dir])


this_path = here
rdkit_path = get_path_from_env("RDKITDIR")
zlib_path = get_path_from_env("ZLIBDIR")
boost_path = get_path_from_env("BOOSTDIR")
eigen_path = get_path_from_env("EIGENDIR")
swig_path = get_path_from_env("SWIG_DIR")
freetype_path = get_path_from_env("FREETYPEDIR")
number_of_processors = os.environ["NUMBER_OF_PROCESSORS"]
minor_version = os.environ["MINORVERSION"] if "MINORVERSION" in os.environ else "1"

_platform_to_g_option_catalog: Mapping[str, str] = {
    "x86": "Visual Studio 15 2017",
    "x64": "Visual Studio 15 2017 Win64",
}

_platform_to_ms_form: Mapping[str, str] = {
    "x86": "Win32",
    "x64": "x64",
}

_platform_to_address_model: Mapping[str, str] = {
    "x86": "32",
    "x64": "64",
}


def _get_value_from_dict(dic: Mapping[str, str], key: Optional[str]) -> str:
    if key is None:
        raise ValueError
    if key not in dic:
        raise ValueError
    return dic[key]


def to_g_option_of_cmake(build_platform: str) -> str:

    if build_platform not in _platform_to_g_option_catalog:
        raise ValueError
    return _platform_to_g_option_catalog[build_platform]


class Config(object):
    def __init__(
        self, build_platform: Optional[str] = None,
    ):
        self.build_platform = build_platform

    @property
    def g_option_of_cmake(self) -> str:
        return _get_value_from_dict(_platform_to_g_option_catalog, self.build_platform)

    def get_build_dir_name(self, build_platform: Optional[str] = None) -> str:
        if build_platform is None:
            build_platform = self.build_platform
        if not build_platform:
            raise ValueError
        return f"build{build_platform}"

    def get_build_dir_name_for_csharp(
        self, build_platform: Optional[str] = None
    ) -> str:
        if build_platform is None:
            build_platform = self.build_platform
        if not build_platform:
            raise ValueError
        return f"build{build_platform}CSharp"

    @property
    def ms_build_platform(self) -> str:
        return _get_value_from_dict(_platform_to_ms_form, self.build_platform)

    @property
    def address_model(self) -> str:
        return _get_value_from_dict(_platform_to_address_model, self.build_platform)

    @property
    def boost_bin_path(self) -> Path:
        assert boost_path
        return boost_path / f"lib{build_platform}-msvc-14.1"

    @property
    def zlib_lib_path(self) -> Path:
        assert zlib_path
        return zlib_path / self.get_build_dir_name() / "Release" / "zlib.lib"

    @property
    def rdkit_csharp_build_path(self) -> Path:
        assert rdkit_path
        return rdkit_path / self.get_build_dir_name_for_csharp()

    @property
    def rdkit_csharp_wrapper_path(self) -> Path:
        assert rdkit_path
        return rdkit_path / "Code" / "JavaWrappers" / "csharp_wrapper"

    @property
    def rdkit_swig_csharp_path(self) -> Path:
        return self.rdkit_csharp_wrapper_path / "swig_csharp"

    def get_rdkit_version(self) -> int:
        return int(re.sub(r".*_(\d\d\d\d)_(\d\d)_(\d)", r"\1\2\3", str(rdkit_path)))

    def get_version_for_nuget(self) -> str:
        return f"0.{self.get_rdkit_version()}.{minor_version}"

    def get_version_for_boost(self) -> str:
        return re.sub(r".*(\d+_\d+_\d+)", r"\1", str(boost_path))

    def get_version_for_eigen(self) -> str:
        return re.sub(r".*(\d+\.\d+\.\d+)", r"\1", str(eigen_path))


def replace_file_string(filename, pattern_replace):
    with open(filename, "r", encoding="utf-8") as file:
        filedata = file.read()
        for pattern, replace in pattern_replace:
            filedata = re.sub(
                pattern, replace, filedata, flags=re.MULTILINE | re.DOTALL
            )
    with open(filename, "w", encoding="utf-8") as file:
        file.write(filedata)


def call_subprocess(cmd: str) -> None:
    try:
        print(cmd)
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(e.returncode)


def _get_cmake_rdkit_cmd_line(config: Config) -> str:
    cmd = (
        "cmake "
        + f"{rdkit_path} "
        + f'-G"{config.g_option_of_cmake}" '
        + "-DRDK_BUILD_SWIG_WRAPPERS=ON "
        + "-DRDK_BUILD_SWIG_CSHARP_WRAPPER=ON "
        + "-DRDK_BUILD_SWIG_JAVA_WRAPPER=OFF "
        + "-DRDK_BUILD_PYTHON_WRAPPERS=OFF "
        + f"-DBOOST_ROOT={str(boost_path)} "
        + f"-DBOOST_INCLUDEDIR={str(boost_path)} "
        + f"-DBOOST_LIBRARYDIR={str(config.boost_bin_path)} "
        + f"-DZLIB_LIBRARY={str(zlib_path)} "
        + f"-DZLIB_INCLUDE_DIR={str(zlib_path)} "
        + f"-DEIGEN3_INCLUDE_DIR={str(eigen_path)} "
        + "-DRDK_INSTALL_INTREE=OFF "
        + "-DRDK_BUILD_CPP_TESTS=ON "
        + "-DRDK_USE_BOOST_REGEX=ON "
        + "-DRDK_BUILD_COORDGEN_SUPPORT=ON "
        + "-DRDK_BUILD_MAEPARSER_SUPPORT=ON "
        + "-DRDK_OPTIMIZE_POPCNT=ON "
        + "-DRDK_BUILD_FREESASA_SUPPORT=OFF "
        + "-DRDK_BUILD_CAIRO_SUPPORT=OFF "
        + "-DRDK_BUILD_THREADSAFE_SSS=ON "
        + "-DRDK_BUILD_INCHI_SUPPORT=ON "
        + "-DRDK_BUILD_AVALON_SUPPORT=ON "
    )

    if config.get_rdkit_version() < 2020091:
        cmd = cmd
    else:
        # freetype supports starts from 2020_09_1
        assert freetype_path
        cmd += (
            ""
            + "-DRDK_SWIG_STATIC=OFF "
            + "-DRDK_INSTALL_STATIC_LIBS=OFF "
            + "-DRDK_INSTALL_DLLS_MSVC=ON "
            + f"-DFREETYPE_LIBRARY={freetype_path / 'objs' / config.ms_build_platform / 'Release' / 'freetype.lib'} "
            + f"-DFREETYPE_INCLUDE_DIRS={freetype_path / 'include'} "
            + "-DRDK_BUILD_TEST_GZIP=OFF "
            + "-DRDK_USE_URF=ON "
        )
    return cmd

def _make_rdkit_cmake(config: Config) -> None:
    cmd = _get_cmake_rdkit_cmd_line(config)
    cmd = cmd.replace("\\", "/")
    call_subprocess(cmd)    

def _build_rdkit_native(config: Config) -> None:
    cmd = f"MSBuild RDKit.sln /p:Configuration=Release,Platform={config.ms_build_platform} /maxcpucount"
    call_subprocess(cmd)

def _copy_fix_to_csharp_wrapper(config: Config) -> None:
    assert config.rdkit_csharp_wrapper_path and config.build_platform
    dll_dest_path = config.rdkit_csharp_wrapper_path / config.build_platform
    if dll_dest_path.exists():
        shutil.rmtree(dll_dest_path)
    dll_dest_path.mkdir()

    # copy "RDKFuncs.dll"
    shutil.copy2(
        config.rdkit_csharp_build_path
        / "Code"
        / "JavaWrappers"
        / "csharp_wrapper"
        / "Release"
        / "RDKFuncs.dll",
        dll_dest_path,
    )
    # copy rdkit dlls
    if config.get_rdkit_version() >= 2020091:
        for filename in glob.glob(
            str(config.rdkit_csharp_build_path / "bin" / "Release" / "*.dll")
        ):
            shutil.copy2(filename, dll_dest_path)

    # copy boost dlls
    assert boost_path
    for filename in glob.glob(
        str(boost_path / f"lib{config.address_model}-msvc-14.1" / "*.dll")
    ):
        if re.match(".*\-vc141\-mt\-x(32|64)\-\d_\d\d\.dll", filename):
            shutil.copy2(filename, dll_dest_path)

    # copy fonttype
    if config.get_rdkit_version() >= 2020091:
        assert freetype_path
        for filename in glob.glob(
            str(
                freetype_path
                / "objs"
                / config.ms_build_platform
                / "Release"
                / "*.dll"
            )
        ):
            shutil.copy2(filename, dll_dest_path)

def _patch_rdkit_swig_files(config: Config) -> None:
    # Customize the followings if required.
    if swig_patch_enabled:
        for filepath, patterns in (
            (
                config.rdkit_swig_csharp_path / "PropertyPickleOptions.cs",
                [("BOOST_BINARY\\(\\s*([01]+)\\s*\\)", "0b\\1")],
            ),
            (
                # remove dupulicated methods.
                config.rdkit_swig_csharp_path / "RDKFuncs.cs",
                [
                    (
                        "public static double DiceSimilarity\\([^\\}]*\\.DiceSimilarity__SWIG_(12|13|14)\\([^\\}]*\\}",
                        "",
                    )
                ],
            ),
        ):
            replace_file_string(filepath, patterns)

    for filepath, patterns in (
        (
            config.rdkit_swig_csharp_path / "RDKFuncsPINVOKE.cs",
            [
                (
                    "(partial )?class RDKFuncsPINVOKE\\s*\\{",
                    "partial class RDKFuncsPINVOKE {",
                )
            ],
        ),
        (
            config.rdkit_swig_csharp_path / "RDKFuncsPINVOKE.cs",
            [
                (
                    "static SWIGExceptionHelper\\(\\)\\s*\\{",
                    "static SWIGExceptionHelper() { RDKFuncsPINVOKE.LoadDll();",
                )
            ],
        ),
    ):
        replace_file_string(filepath, patterns)
    shutil.copy2(
        this_path / "csharp_wrapper" / "RDKFuncsPINVOKE_Loader.cs",
        config.rdkit_swig_csharp_path,
    )


def make_native(config: Config) -> None:
    assert config.build_platform
    config.rdkit_csharp_build_path.mkdir(exist_ok=True)
    _curdir = os.curdir
    os.chdir(config.rdkit_csharp_build_path)
    try:
        if swig_patch_enabled:
            assert rdkit_path
            replace_file_string(
                str(
                    rdkit_path
                    / "Code"
                    / "JavaWrappers"
                    / "csharp_wrapper"
                    / "GraphMolCSharp.i"
                ),
                [("boost::int32_t", "int32_t"), ("boost::uint32_t", "uint32_t")],
            )
        _make_rdkit_cmake(config)
        _build_rdkit_native(config)
        _copy_fix_to_csharp_wrapper(config)
    finally:
        os.chdir(_curdir)


def build_csharp_wrapper(config: Config) -> None:
    _patch_rdkit_swig_files(config)       

    path_RDKit2DotNet_csproj = config.rdkit_csharp_wrapper_path / "RDKit2DotNet.csproj"
    replace_file_string(
        str(path_RDKit2DotNet_csproj),
        [
            (
                r"\<Content Include\=\"RDKFuncs\.dll\"\>.*\<\/Content\>",
                r'<Content Include="x64\\RDKFuncs.dll"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></Content>'  # NOQA
                r'<Content Include="x86\\RDKFuncs.dll"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></Content>',  # NOQA
            )
        ],
    )
    for src, dst in (
        (
            this_path / "csharp_wrapper" / "RDKitCSharpTest.csproj",
            config.rdkit_csharp_wrapper_path / "RDKitCSharpTest",
        ),
        (
            this_path / "csharp_wrapper" / "RDKit2DotNet.sln",
            config.rdkit_csharp_wrapper_path,
        ),
    ):
        shutil.copy2(src, dst)

    print(
        f"Solution file '{config.rdkit_csharp_wrapper_path / 'RDKit2DotNet.sln'}' is created."
    )
    # if required modifiy followings.
    # - Remove duplicated methods.
    # - Rename miss named SWIGTYPE classes.
    # - Add version infomation.
    # - Sign."

    _pushd_build_wrapper = os.getcwd()
    try:
        os.chdir(config.rdkit_csharp_wrapper_path)
        cmd = "MSBuild RDKit2DotNet.csproj /p:Configuration=Release,Platform=AnyCPU /maxcpucount"
        call_subprocess(cmd)
    finally:
        os.chdir(_pushd_build_wrapper)


def build_nuget_package(config: Config) -> None:
    dll_basenames_dic: Dict[str, List[str]] = dict()
    for cpu_model in cpu_models:
        dlls_path = config.rdkit_csharp_wrapper_path / cpu_model
        dll_basenames: List[str] = []
        for filename in glob.glob(str(dlls_path / "*.dll")):
            dll_basenames.append(os.path.basename(filename))
        dll_basenames_dic[cpu_model] = dll_basenames

    # Prepare RDKit2DotNet.nuspec

    nuspec_file = shutil.copy(
        this_path / "csharp_wrapper" / f"{project_name}.nuspec",
        config.rdkit_csharp_wrapper_path,
    )

    replace_file_string(
        nuspec_file,
        [
            (
                "\\<version\\>[0-9\\.]*\\<\\/version\\>",
                f"<version>{config.get_version_for_nuget()}</version>",
            )
        ],
    )
    replace_file_string(
        nuspec_file,
        [
            (
                "RDKit Release_\\d\\d\\d\\d\\_\\d\\d\\_\\d",
                f"RDKit Release_{config.get_version_for_nuget().replace('.', '_')}",
            )
        ],
    )
    replace_file_string(
        nuspec_file,
        [("Boost \\d+\\.\\d+\\.\\d+", f"Boost {config.get_version_for_boost()}")],
    )
    replace_file_string(
        nuspec_file,
        [("Eigen \\d+\\.\\d+\\.\\d+", f"Eigen {config.get_version_for_eigen()}")],
    )

    nuspec_dlls_spec = []
    for cpu_model in cpu_models:
        for dll_basename in dll_basenames_dic[cpu_model]:
            nuspec_dlls_spec.append(
                f'<file src="{cpu_model}/{dll_basename}" target="runtimes/win-{cpu_model}/native" />\n'
            )

    print("".join(nuspec_dlls_spec))
    replace_file_string(
        nuspec_file, [("\\<nativefiles\\s*\\/\\>", "".join(nuspec_dlls_spec))]
    )

    targets_file = shutil.copy(
        this_path / "csharp_wrapper" / f"{project_name}.targets",
        config.rdkit_csharp_wrapper_path,
    )
    targets_dlls_spec: List[str] = []
    for cpu_model in cpu_models:
        targets_dlls_spec.append(
            f"<ItemGroup Condition=\" '$(Platform)' == '{cpu_model}' \">\\n"
        )
        for dllname in dll_basenames_dic[cpu_model]:
            targets_dlls_spec.append(
                f'<None Include="$(MSBuildThisFileDirectory)../runtimes/win-{cpu_model}/native/{dllname}">\\n'
            )
            targets_dlls_spec.append(f"<Link>{dllname}</Link>\\n")
            targets_dlls_spec.append(
                "<CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>\\n"
            )
            targets_dlls_spec.append("</None>\\n")
        targets_dlls_spec.append("</ItemGroup>\\n")

    targets_dlls_spec.append("<ItemGroup Condition=\" '$(Platform)' == 'AnyCPU' \">\\n")

    for cpu_model in cpu_models:
        for dllname in dll_basenames_dic[cpu_model]:
            targets_dlls_spec.append(
                f'<None Include="$(MSBuildThisFileDirectory)../runtimes/win-{cpu_model}/native/{dllname}">\\n'
            )
            targets_dlls_spec.append(f"<Link>{cpu_model}/{dllname}</Link>\\n")
            targets_dlls_spec.append(
                "<CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>\\n"
            )
            targets_dlls_spec.append("</None>\\n")

    targets_dlls_spec.append("</ItemGroup>")
    replace_file_string(
        targets_file, [("\\<nativefiles\\s*\\/\\>", "".join(targets_dlls_spec))]
    )

    _curr_dir = os.curdir
    os.chdir(config.rdkit_csharp_wrapper_path)
    try:
        cmd = f'nuget pack "{project_name}.nuspec" -Prop Configuration=Release -IncludeReferencedProjects'
        call_subprocess(cmd)
    finally:
        os.chdir(_curr_dir)


if __name__ == "__main__":
    build_platform: Optional[str] = None
    if "BUILDPLATFORM" in os.environ:
        build_platform = os.environ["BUILDPLATFORM"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--build_platform", choices=("x86", "x64", "all"), default=build_platform,
    )
    parser.add_argument(
        "--disable_swig_patch", default=False, action="store_true",
    )
    parser.add_argument(
        "--make_native", default=False, action="store_true",
    )
    parser.add_argument(
        "--build_wrapper", default=False, action="store_true",
    )
    parser.add_argument(
        "--build_nuget", default=False, action="store_true",
    )
    args = parser.parse_args()

    swig_patch_enabled = not args.disable_swig_patch

    curr_dir = os.getcwd()
    try:
        if args.make_native:
            if args.build_platform == "all":
                for platform in (
                    "x86",
                    "x64",
                ):
                    make_native(Config(build_platform=platform))
            else:
                make_native(Config(build_platform=args.build_platform))
        if args.build_wrapper:
            build_csharp_wrapper(Config())
        if args.build_nuget:
            build_nuget_package(Config())
    finally:
        os.chdir(curr_dir)
