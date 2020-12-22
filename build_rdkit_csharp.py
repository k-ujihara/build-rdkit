"""Script to make RDKit.DotNetWrapper.

Notes:
    This is tested for rdkit-Release_2019.09.1 and 2020.09.1
"""

import argparse
import glob
import logging
import os
import pathlib
import re
import shutil
import subprocess
import sys
from os import PathLike
from pathlib import Path
from typing import Any, Dict, List, Mapping, NamedTuple, Optional, Sequence, Union, cast

logging.basicConfig(level=logging.DEBUG)

project_name: str = "RDKit.DotNetWrap"


here = Path(__file__).parent.resolve()
cpu_models: Sequence[str] = (
    "x86",
    "x64",
)
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


def get_value(dic: Mapping[str, str], key: Optional[str]) -> str:
    if key is None:
        raise ValueError
    if key not in dic:
        raise ValueError
    return dic[key]


def replace_file_string(filename, pattern_replace, make_backup: bool = False):
    bak_filename = f"{filename}.bak"
    if os.path.exists(bak_filename):
        shutil.copy(bak_filename, filename)
    with open(filename, "r", encoding="utf-8") as file:
        filedata = file.read()
        for pattern, replace in pattern_replace:
            filedata = re.sub(
                pattern, replace, filedata, flags=re.MULTILINE | re.DOTALL
            )
    if make_backup:
        shutil.copy(filename, bak_filename)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(filedata)


def call_subprocess(cmd: str) -> None:
    try:
        _env: Dict[str, str] = {}
        _env.update(os.environ)
        _CL_env_for_MSVC: Mapping[str, str] = {
            "CL": "/source-charset:utf-8 /execution-charset:utf-8"
        }
        _env.update(_CL_env_for_MSVC)
        logging.info(cmd)
        subprocess.check_call(cmd, env=_env)
    except subprocess.CalledProcessError as e:
        logging.warn(e)
        sys.exit(e.returncode)


def remove_if_exist(path: Path):
    if path.exists():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


class Config(NamedTuple):
    this_path: Optional[Path] = None
    rdkit_path: Optional[Path] = None
    boost_path: Optional[Path] = None
    eigen_path: Optional[Path] = None
    zlib_path: Optional[Path] = None
    libpng_path: Optional[Path] = None
    pixman_path: Optional[Path] = None
    cairo_path: Optional[Path] = None
    swig_path: Optional[Path] = None
    freetype_path: Optional[Path] = None
    number_of_processors: int = 1
    minor_version: int = 1
    cairo_support: bool = False
    swig_patch_enabled: bool = True


class NativeMaker:
    def __init__(self, config: Config, build_platform: Optional[str] = None):
        self.build_platform: Optional[str] = build_platform
        self.config = config

    @property
    def g_option_of_cmake(self) -> str:
        return get_value(_platform_to_g_option_catalog, self.build_platform)

    @property
    def build_dir_name(self) -> str:
        assert self.build_platform
        return f"build{self.build_platform}"

    @property
    def build_dir_name_for_csharp(self) -> str:
        assert self.build_platform
        return f"build{self.build_platform}CSharp"

    @property
    def ms_build_platform(self) -> str:
        return get_value(_platform_to_ms_form, self.build_platform)

    @property
    def address_model(self) -> str:
        return get_value(_platform_to_address_model, self.build_platform)

    @property
    def this_path(self) -> Path:
        assert self.config.this_path
        return self.config.this_path

    @property
    def rdkit_path(self) -> Path:
        assert self.config.rdkit_path
        return self.config.rdkit_path

    @property
    def boost_path(self) -> Path:
        assert self.config.boost_path
        return self.config.boost_path

    @property
    def eigen_path(self) -> Path:
        assert self.config.eigen_path
        return self.config.eigen_path

    @property
    def zlib_path(self) -> Path:
        assert self.config.zlib_path
        return self.config.zlib_path

    @property
    def libpng_path(self) -> Path:
        assert self.config.libpng_path
        return self.config.libpng_path

    @property
    def pixman_path(self) -> Path:
        assert self.config.pixman_path
        return self.config.pixman_path

    @property
    def freetype_path(self) -> Path:
        assert self.config.freetype_path
        return self.config.freetype_path

    @property
    def cairo_path(self) -> Path:
        assert self.config.cairo_path
        return self.config.cairo_path

    @property
    def boost_bin_path(self) -> Path:
        return self.boost_path / f"lib{self.build_platform}-msvc-14.1"

    @property
    def rdkit_csharp_build_path(self) -> Path:
        return self.rdkit_path / self.build_dir_name_for_csharp

    @property
    def rdkit_csharp_wrapper_path(self) -> Path:
        return self.rdkit_path / "Code" / "JavaWrappers" / "csharp_wrapper"

    @property
    def rdkit_swig_csharp_path(self) -> Path:
        return self.rdkit_csharp_wrapper_path / "swig_csharp"

    def get_rdkit_version(self) -> int:
        return int(
            re.sub(r".*_(\d\d\d\d)_(\d\d)_(\d)", r"\1\2\3", str(self.config.rdkit_path))
        )

    def get_version_for_nuget(self) -> str:
        return f"0.{self.get_rdkit_version()}.{self.config.minor_version}"

    def get_version_for_rdkit(self) -> str:
        num = self.get_rdkit_version()
        return f"{num // 1000}_{('00' + str((num % 1000) // 10))[-2:]}_{num % 10}"

    def get_version_for_boost(self) -> str:
        return re.sub(r".*(\d+_\d+_\d+)", r"\1", str(self.boost_path))

    def get_version_for_eigen(self) -> str:
        return re.sub(r".*(\d+\.\d+\.\d+)", r"\1", str(self.eigen_path))

    def get_version_for_zlib(self) -> str:
        return re.sub(r".*(\d+\.\d+\.\d+)", r"\1", str(self.zlib_path))

    def get_version_for_libpng(self) -> str:
        return re.sub(r".*lpng(\d)(\d)(\d\d)", r"\1.\2.\3", str(self.libpng_path))

    def get_version_for_freetype(self) -> str:
        return re.sub(r".*(\d+\.\d+\.\d+)", r"\1", str(self.freetype_path))

    def get_version_for_pixman(self) -> str:
        return re.sub(r".*(\d+\.\d+\.\d+)", r"\1", str(self.pixman_path))

    def get_version_for_cairo(self) -> str:
        return re.sub(r".*(\d+\.\d+\.\d+)", r"\1", str(self.cairo_path))

    def _get_cmake_rdkit_cmd_line(self) -> str:
        cmd = (
            "cmake "
            + f"{str(self.rdkit_path)} "
            + f'-G"{self.g_option_of_cmake}" '
            + "-DRDK_BUILD_SWIG_WRAPPERS=ON "
            + "-DRDK_BUILD_SWIG_CSHARP_WRAPPER=ON "
            + "-DRDK_BUILD_SWIG_JAVA_WRAPPER=OFF "
            + "-DRDK_BUILD_PYTHON_WRAPPERS=OFF "
            + (
                (
                    f"-DBOOST_ROOT={str(self.boost_path)} "
                    + f"-DBOOST_INCLUDEDIR={str(self.boost_path)} "
                    + f"-DBOOST_LIBRARYDIR={str(self.boost_bin_path)} "
                )
                if self.config.boost_path
                else ""
            )
            + (
                f"-DEIGEN3_INCLUDE_DIR={str(self.eigen_path)} "
                if self.config.eigen_path
                else ""
            )
            + "-DRDK_INSTALL_INTREE=OFF "
            + "-DRDK_BUILD_CPP_TESTS=ON "
            + "-DRDK_USE_BOOST_REGEX=ON "
            + "-DRDK_BUILD_COORDGEN_SUPPORT=ON "
            + "-DRDK_BUILD_MAEPARSER_SUPPORT=ON "
            + "-DRDK_OPTIMIZE_POPCNT=ON "
            + "-DRDK_BUILD_FREESASA_SUPPORT=OFF "
            + "-DRDK_BUILD_THREADSAFE_SSS=ON "
            + "-DRDK_BUILD_INCHI_SUPPORT=ON "
            + "-DRDK_BUILD_AVALON_SUPPORT=ON "
            + "-DRDK_BUILD_CAIRO_SUPPORT=ON "
            + f'-DCAIRO_INCLUDE_DIRS={self.cairo_path / "src"} '
            + f'-DCAIRO_LIBRARIES={self.cairo_path / "vc2017" / self.ms_build_platform / "Release" / "cairo.lib"} '
        )

        if self.get_rdkit_version() >= 2020091:
            # freetype supports starts from 2020_09_1
            assert self.config.freetype_path
            cmd += (
                ""
                + "-DRDK_SWIG_STATIC=OFF "
                + "-DRDK_INSTALL_STATIC_LIBS=OFF "
                + "-DRDK_INSTALL_DLLS_MSVC=ON "
                + (
                    (
                        f"-DFREETYPE_LIBRARY={self.freetype_path / 'objs' / self.ms_build_platform / 'Release' / 'freetype.lib'} "
                        + f"-DFREETYPE_INCLUDE_DIRS={self.freetype_path / 'include'} "
                    )
                    if self.config.freetype_path
                    else ""
                )
                + "-DRDK_BUILD_TEST_GZIP=OFF "
                + "-DRDK_USE_URF=ON "
            )
        return cmd

    def _make_rdkit_cmake(self) -> None:
        cmd = self._get_cmake_rdkit_cmd_line()
        cmd = cmd.replace("\\", "/")
        call_subprocess(cmd)

    def _build_rdkit_native(self) -> None:
        self.run_msbuild("RDKit.sln")

    def _copy_to_csharp_wrapper(self) -> None:
        assert self.build_platform
        dll_dest_path = self.rdkit_csharp_wrapper_path / self.build_platform
        remove_if_exist(dll_dest_path)
        dll_dest_path.mkdir()
        logging.info(f"Copy DLLs to {dll_dest_path}.")

        files_to_copy: List[Union[str, PathLike]] = []

        # copy "RDKFuncs.dll"
        files_to_copy.append(
            self.rdkit_csharp_build_path
            / "Code"
            / "JavaWrappers"
            / "csharp_wrapper"
            / "Release"
            / "RDKFuncs.dll"
        )

        # copy rdkit dlls from 2020_09_1 submodules are separated
        if self.get_rdkit_version() >= 2020091:
            for filename in glob.glob(
                str(self.rdkit_csharp_build_path / "bin" / "Release" / "*.dll")
            ):
                files_to_copy.append(filename)

        # copy boost dlls
        for filename in glob.glob(
            str(self.boost_path / f"lib{self.address_model}-msvc-14.1" / "*.dll")
        ):
            if re.match(r".*\-vc141\-mt\-x(32|64)\-\d_\d\d\.dll", filename):
                if not os.path.basename(filename).startswith("boost_python"):
                    files_to_copy.append(filename)

        # copy fonttype
        if self.config.cairo_support or self.get_rdkit_version() >= 2020091:
            files_to_copy.append(
                self.freetype_path
                / "objs"
                / self.ms_build_platform
                / "Release"
                / "freetype.dll"
            )

        if self.config.cairo_support:
            files_to_copy += [
                self.zlib_path / self.build_dir_name / "Release" / "zlib.dll",
                self.libpng_path / self.build_dir_name / "Release" / "libpng16.dll",
                self.pixman_path
                / "vc2017"
                / self.ms_build_platform
                / "Release"
                / "pixman.dll",
                self.cairo_path
                / "vc2017"
                / self.ms_build_platform
                / "Release"
                / "cairo.dll",
            ]

        for path in files_to_copy:
            shutil.copy2(path, dll_dest_path)

    def _patch_rdkit_swig_files(self) -> None:
        # Customize the followings if required.
        if self.config.swig_patch_enabled:
            for filepath, patterns in (
                (
                    self.rdkit_swig_csharp_path / "PropertyPickleOptions.cs",
                    [("BOOST_BINARY\\(\\s*([01]+)\\s*\\)", "0b\\1")],
                ),
                (
                    # remove dupulicated methods.
                    self.rdkit_swig_csharp_path / "RDKFuncs.cs",
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
                self.rdkit_swig_csharp_path / "RDKFuncsPINVOKE.cs",
                [
                    (
                        "(partial )?class RDKFuncsPINVOKE\\s*\\{",
                        "partial class RDKFuncsPINVOKE {",
                    )
                ],
            ),
            (
                self.rdkit_swig_csharp_path / "RDKFuncsPINVOKE.cs",
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
            self.this_path / "csharp_wrapper" / "RDKFuncsPINVOKE_Loader.cs",
            self.rdkit_swig_csharp_path,
        )

    def run_msbuild(
        self, proj: Union[PathLike, str], platform: Optional[str] = None
    ) -> None:
        if not platform:
            platform = self.ms_build_platform
        cmd = (
            f"MSBuild {proj} /p:Configuration=Release,Platform={platform} /maxcpucount"
        )
        call_subprocess(cmd)

    def make_zlib(self) -> None:
        build_path = self.zlib_path / self.build_dir_name
        build_path.mkdir(exist_ok=True)
        _curdir = os.path.abspath(os.curdir)
        try:
            os.chdir(build_path)
            cmd = f'cmake {str(self.zlib_path)} -G"{self.g_option_of_cmake}" '
            call_subprocess(cmd)
            self.run_msbuild("zlib.sln")
            shutil.copy2(build_path / "zconf.h", self.zlib_path)
        finally:
            os.chdir(_curdir)

    def make_libpng(self) -> None:
        build_path = self.libpng_path / self.build_dir_name
        build_path.mkdir(exist_ok=True)
        _curdir = os.path.abspath(os.curdir)
        try:
            os.chdir(build_path)
            cmd = (
                "cmake "
                + f"{str(self.libpng_path)} "
                + f'-G"{self.g_option_of_cmake}" '
                + f'-DZLIB_LIBRARY="{str(self.zlib_path / self.build_dir_name / "Release" / "zlib.lib")}" '
                + f'-DZLIB_INCLUDE_DIR="{str(self.zlib_path)}" '
                + "-DPNG_SHARED=ON "
                + "-DPNG_STATIC=OFF "
            )
            call_subprocess(cmd)
            self.run_msbuild("libpng.sln")
        finally:
            os.chdir(_curdir)

    def make_pixman(self) -> None:
        _curdir = os.path.abspath(os.curdir)
        try:
            proj_dir = self.pixman_path / "vc2017"
            proj_dir.mkdir(exist_ok=True)
            os.chdir(proj_dir)
            files_dir = self.this_path / "files" / "pixman"
            vcxproj = "pixman.vcxproj"
            shutil.copy2(files_dir / vcxproj, proj_dir)
            proj_file = proj_dir / vcxproj
            shutil.copy2(files_dir / "config.h", self.pixman_path / "pixman")
            makefile_win32 = self.pixman_path / "pixman" / "Makefile.win32"
            makefile_sources = self.pixman_path / "pixman" / "Makefile.sources"

            class ClAdder:
                def __init__(self, str_Cls: List[str], pattern: str):
                    self.str_Cls: List[str] = str_Cls
                    self.regex = re.compile(pattern)

                def add_if_match(self, line: str) -> None:
                    match = self.regex.match(line)
                    if match:
                        name = match[1]
                        if name.endswith(".c"):
                            self.str_Cls.append(
                                f'<ClCompile Include="..\pixman\{name}" />\n'
                            )
                        elif name.endswith(".h"):
                            self.str_Cls.append(
                                f'<ClInclude Include="..\pixman\{name}" />\n'
                            )

            str_Cls: List[str] = []
            adder = ClAdder(str_Cls, "^\\s+([A-Za-z0-9\-]+\\.(c|h))\\b.*$")
            with open(makefile_sources, "r") as f:
                for line in f.readlines():
                    adder.add_if_match(line)
            adder = ClAdder(
                str_Cls,
                "^\\s*libpixman_sources\\s*\\+\\=\\s*([A-Za-z0-9\-]+\\.(c|h))\\b.*$",
            )
            with open(makefile_win32, "r") as f:
                for line in f.readlines():
                    print(line)
                    adder.add_if_match(line)
            replace_file_string(
                proj_file,
                [("<PLACEHOLDER\\s*\/>", "".join(str_Cls).replace("\\", "\\\\"),)],
            )
            self.run_msbuild(vcxproj)
        finally:
            os.chdir(_curdir)

    def make_cairo(self) -> None:
        # TODO: get file names from src\Makefile.sources
        _curdir = os.path.abspath(os.curdir)
        try:
            proj_dir = self.cairo_path / "vc2017"
            proj_dir.mkdir(exist_ok=True)
            os.chdir(proj_dir)
            files_dir = self.this_path / "files" / "cairo"
            vcxproj = "cairo.vcxproj"
            shutil.copy2(files_dir / vcxproj, proj_dir)
            proj_file = proj_dir / vcxproj
            shutil.copy2(files_dir / "cairo-features.h", self.cairo_path / "src")
            replace_file_string(
                proj_file,
                [
                    ("__CAIRODIR__", str(self.cairo_path).replace("\\", "\\\\"),),
                    ("__LIBPNGDIR__", str(self.libpng_path).replace("\\", "\\\\"),),
                    ("__ZLIBDIR__", str(self.zlib_path).replace("\\", "\\\\"),),
                    ("__PIXMANDIR__", str(self.pixman_path).replace("\\", "\\\\"),),
                    ("__FREETYPEDIR__", str(self.freetype_path).replace("\\", "\\\\"),),
                ],
            )
            self.run_msbuild(vcxproj)
        finally:
            os.chdir(_curdir)

    def make_freetype(self) -> None:
        _curdir = os.path.abspath(os.curdir)
        try:
            os.chdir(self.freetype_path)
            shutil.copy2(
                self.this_path / "files" / "freetype.vcxproj",
                self.freetype_path / "builds" / "windows" / "vc2010",
            )
            os.chdir(self.freetype_path / "builds" / "windows" / "vc2010")
            logging.debug(f"current dir = {os.getcwd()}")
            self.run_msbuild("freetype.sln")
        finally:
            os.chdir(_curdir)

    def build_rdkit(self) -> None:
        self.rdkit_csharp_build_path.mkdir(exist_ok=True)
        _curdir = os.path.abspath(os.curdir)
        os.chdir(self.rdkit_csharp_build_path)
        try:
            if self.config.swig_patch_enabled:
                replace_file_string(
                    self.rdkit_csharp_wrapper_path / "GraphMolCSharp.i",
                    [("boost::int32_t", "int32_t",), ("boost::uint32_t", "uint32_t",)],
                    make_backup=True,
                )
            self._make_rdkit_cmake()
            self._build_rdkit_native()
            self._copy_to_csharp_wrapper()
        finally:
            os.chdir(_curdir)

    def build_csharp_wrapper(self) -> None:
        self._patch_rdkit_swig_files()
        path_RDKit2DotNet_csproj = (
            self.rdkit_csharp_wrapper_path / "RDKit2DotNet.csproj"
        )

        contents_replaced = ""
        for cpu_model in cpu_models:
            for filename in glob.glob(
                str(self.rdkit_csharp_wrapper_path / cpu_model / "*.dll")
            ):
                basename = os.path.basename(filename)
                contents_replaced += f'<Content Include="{cpu_model}\\\\{basename}"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></Content>\n'
        replace_file_string(
            path_RDKit2DotNet_csproj,
            [
                (
                    r"\<Content Include\=\"RDKFuncs\.dll\"\>.*\<\/Content\>",
                    contents_replaced,
                )
            ],
            make_backup=True,
        )

        for src, dst in (
            (
                self.this_path / "csharp_wrapper" / "RDKitCSharpTest.csproj",
                self.rdkit_csharp_wrapper_path / "RDKitCSharpTest",
            ),
            (
                self.this_path / "csharp_wrapper" / "RDKit2DotNet.sln",
                self.rdkit_csharp_wrapper_path,
            ),
        ):
            shutil.copy2(src, dst)

        print(
            f"Solution file '{self.rdkit_csharp_wrapper_path / 'RDKit2DotNet.sln'}' is created."
        )
        # if required modifiy followings.
        # - Remove duplicated methods.
        # - Rename miss named SWIGTYPE classes.
        # - Add version infomation.
        # - Sign."

        _pushd_build_wrapper = os.getcwd()
        try:
            os.chdir(self.rdkit_csharp_wrapper_path)
            self.run_msbuild("RDKit2DotNet.csproj", "AnyCPU")
        finally:
            os.chdir(_pushd_build_wrapper)

    def build_nuget_package(self) -> None:
        dll_basenames_dic: Dict[str, List[str]] = dict()
        for cpu_model in cpu_models:
            dlls_path = self.rdkit_csharp_wrapper_path / cpu_model
            dll_basenames: List[str] = []
            for filename in glob.glob(str(dlls_path / "*.dll")):
                dll_basenames.append(os.path.basename(filename))
            dll_basenames_dic[cpu_model] = dll_basenames

        # Prepare RDKit2DotNet.nuspec

        nuspec_file = shutil.copy(
            self.this_path / "csharp_wrapper" / f"{project_name}.nuspec",
            self.rdkit_csharp_wrapper_path,
        )

        # RDKit Release_0000_00_0, Boost 0.0.0, FreeType 0.0.0, and Eigen 0.0.0
        lib_versions: List[str] = [
            f"Boost {self.get_version_for_boost()}",
            f"Eigen {self.get_version_for_eigen()}",
            f"FreeType {self.get_version_for_freetype()}",
        ]
        if self.config.cairo_support:
            lib_versions += [
                f"zlib {self.get_version_for_zlib()}",
                f"libpng {self.get_version_for_libpng()}",
                f"pixman {self.get_version_for_pixman()}",
                f"cairo {self.get_version_for_cairo()}",
            ]
        replace_file_string(
            nuspec_file,
            [
                (
                    "\\<version\\>[0-9\\.]*\\<\\/version\\>",
                    f"<version>{self.get_version_for_nuget()}</version>",
                ),
                ("__RDKITVERSION__", f"{self.get_version_for_rdkit()}",),
                ("__LIBVERSIONS__", ", ".join(lib_versions),),
            ],
        )

        nuspec_dlls_spec = []
        for cpu_model in cpu_models:
            for dll_basename in dll_basenames_dic[cpu_model]:
                nuspec_dlls_spec.append(
                    f'<file src="{cpu_model}/{dll_basename}" target="runtimes/win-{cpu_model}/native" />\n'
                )

        replace_file_string(
            nuspec_file, [("\\<nativefiles\\s*\\/\\>", "".join(nuspec_dlls_spec))]
        )

        targets_file = shutil.copy(
            self.this_path / "csharp_wrapper" / f"{project_name}.targets",
            self.rdkit_csharp_wrapper_path,
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

        targets_dlls_spec.append(
            "<ItemGroup Condition=\" '$(Platform)' == 'AnyCPU' \">\\n"
        )

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
        os.chdir(self.rdkit_csharp_wrapper_path)
        try:
            cmd = f'nuget pack "{project_name}.nuspec" -Prop Configuration=Release -IncludeReferencedProjects'
            call_subprocess(cmd)
        finally:
            os.chdir(_curr_dir)

    def clean(self):
        if self.config.rdkit_path:
            rdkit_path_csharp_wrapper = (
                self.rdkit_path / "Code" / "JavaWrappers" / "csharp_wrapper"
            )
            for p in (
                "RDKit.DotNetWrap.nuspec",
                "RDKit.DotNetWrap.targets",
            ):
                remove_if_exist(rdkit_path_csharp_wrapper / p)
            remove_if_exist(self.rdkit_path / "lib")
            for p in cpu_models:
                remove_if_exist(rdkit_path_csharp_wrapper / p)
                remove_if_exist(self.rdkit_path / f"build{p}CSharp")
        if self.config.freetype_path:
            for p in cpu_models:
                remove_if_exist(self.freetype_path / "objs" / _platform_to_ms_form[p])
        if self.config.zlib_path:
            for p in cpu_models:
                remove_if_exist(self.zlib_path / "zconf.h")
                remove_if_exist(self.zlib_path / f"build{_platform_to_ms_form[p]}")
        if self.config.libpng_path:
            for p in cpu_models:
                remove_if_exist(self.libpng_path / f"build{_platform_to_ms_form[p]}")
        if self.config.pixman_path:
            remove_if_exist(self.pixman_path / f"vc2017")
        if self.config.cairo_path:
            remove_if_exist(self.cairo_path / f"vc2017")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build_platform", choices=("x86", "x64", "all"))
    parser.add_argument("--disable_swig_patch", default=False, action="store_true")
    for opt in (
        "build_zlib",
        "build_libpng",
        "build_pixman",
        "build_freetype",
        "build_cairo",
        "build_rdkit",
        "build_wrapper",
        "build_nuget",
    ):
        parser.add_argument(f"--{opt}", default=False, action="store_true")
    for opt in (
        "rdkit",
        "boost",
        "eigen",
        "zlib",
        "freetype",
        "libpng",
        "pixman",
        "cairo",
    ):
        parser.add_argument(f"--{opt}_dir", type=str)
    parser.add_argument("--clean", default=False, action="store_true")
    args = parser.parse_args()

    def get_value_from_env(env: str, default: Optional[str] = None) -> Optional[str]:
        if env not in os.environ:
            return default
        return os.environ[env]

    def path_from_arg_or_env(arg: Any, env: str) -> Optional[Path]:
        if arg:
            return Path(arg)
        value = get_value_from_env(env)
        return Path(value) if value else None

    config = Config(
        minor_version=cast(int, get_value_from_env("MINOR_VERSION", "1")),
        swig_patch_enabled=not args.disable_swig_patch,
        this_path=here,
        rdkit_path=path_from_arg_or_env(args.rdkit_dir, "RDKIT_DIR"),
        boost_path=path_from_arg_or_env(args.boost_dir, "BOOST_DIR"),
        eigen_path=path_from_arg_or_env(args.eigen_dir, "EIGEN_DIR"),
        zlib_path=path_from_arg_or_env(args.zlib_dir, "ZLIB_DIR"),
        libpng_path=path_from_arg_or_env(args.libpng_dir, "LIBPNG_DIR"),
        pixman_path=path_from_arg_or_env(args.pixman_dir, "PIXMAN_DIR"),
        freetype_path=path_from_arg_or_env(args.freetype_dir, "FREETYPE_DIR"),
        cairo_path=path_from_arg_or_env(args.cairo_dir, "CAIRO_DIR"),
        swig_path=path_from_arg_or_env(None, "SWIG_DIR"),
        number_of_processors=cast(int, get_value_from_env("NUMBER_OF_PROCESSORS", "1")),
        cairo_support=True,
    )

    curr_dir = os.getcwd()
    try:
        if args.clean:
            NativeMaker(config).clean()
        for platform in (
            cpu_models if args.build_platform == "all" else (args.build_platform,)
        ):
            maker = NativeMaker(config, platform)
            if args.build_freetype:
                maker.make_freetype()
            if args.build_zlib:
                maker.make_zlib()
            if args.build_libpng:
                maker.make_libpng()
            if args.build_pixman:
                maker.make_pixman()
            if args.build_cairo:
                maker.make_cairo()
            if args.build_rdkit:
                maker.build_rdkit()
        maker = NativeMaker(config)
        if args.build_wrapper:
            maker.build_csharp_wrapper()
        if args.build_nuget:
            maker.build_nuget_package()
    finally:
        os.chdir(curr_dir)


if __name__ == "__main__":
    main()
