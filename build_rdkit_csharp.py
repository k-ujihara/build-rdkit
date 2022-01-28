"""Script to make RDKit.DotNetWrapper.

Notes:
    This is developed with rdkit-Release_2021_09_4.
"""
from enum import Enum
import argparse
import glob
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
import typing
import xml.etree.ElementTree as ET
from os import PathLike
from pathlib import Path
from subprocess import PIPE
from typing import (
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)
from xml.etree.ElementTree import Element, ElementTree, SubElement

logging.basicConfig(level=logging.DEBUG)
project_name: str = "RDKit.DotNetWrap"

VisualStudioVersion = Literal["15.0", "16.0"]
CpuModel = Literal["x86", "x64"]
MSPlatform = Literal["Win32", "x64"]
AddressModel = Literal[32, 64]
MSVCInternalVersion = Literal["14.1", "14.2"]
SupportedSystem = Literal["win", "linux"]

here = Path(__file__).parent.resolve()

class LangType(Enum):
    CPlusPlus = 1
    Java = 2
    CSharp = 3
    Python = 4

_LangType_to_str: Mapping[LangType, str]  ={
    LangType.CPlusPlus: "cpp",
    LangType.Java: "java",
    LangType.CSharp: "CSharp",
    LangType.Python : "python",
}


_platform_system_to_system: Mapping[str, SupportedSystem] = {
    "Windows": "win",
    "Linux": "linux",
}

_vs_ver_to_cmake_option_catalog: Mapping[VisualStudioVersion, Mapping[CpuModel, Sequence[str]]] = {
    "15.0": {
        "x86": ['-G"Visual Studio 15 2017"'],
        "x64": ['-G"Visual Studio 15 2017 Win64"'],
    },
    "16.0": {
        "x86": ['-G"Visual Studio 16 2019"', "-AWin32"],
        "x64": ['-G"Visual Studio 16 2019"'],
    },
}
_platform_to_ms_form: Mapping[CpuModel, MSPlatform] = {
    "x86": "Win32",
    "x64": "x64",
}
_platform_to_address_model: Mapping[CpuModel, AddressModel] = {
    "x86": 32,
    "x64": 64,
}
_vs_to_msvc_internal_ver: Mapping[VisualStudioVersion, MSVCInternalVersion] = {
    "15.0": "14.1",
    "16.0": "14.2",
}



def get_os() -> SupportedSystem:
    pf = platform.system()
    if pf not in _platform_system_to_system:
        raise RuntimeError
    return _platform_system_to_system[pf]


def get_value(dic: Mapping[str, str], key: Optional[str]) -> str:
    if key is None:
        raise ValueError
    if key not in dic:
        raise ValueError
    return dic[key]


def make_bak(filename: PathLike) -> None:
    bak_filename = f"{filename}.bak"
    if not os.path.exists(bak_filename):
        shutil.copy2(filename, bak_filename)


def restore_from_bak(filename: PathLike) -> None:
    bak_filename = f"{filename}.bak"
    if os.path.exists(bak_filename):
        shutil.copy2(bak_filename, filename)


def get_as_text(filename: PathLike) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        filedata = file.read()
        return filedata


def get_original_text(filename: PathLike) -> str:
    bak_filename = f"{filename}.bak"
    if os.path.exists(bak_filename):
        filename = Path(bak_filename)
    text = get_as_text(filename)
    return text


def _replace_file_content(
    filename: PathLike, replace_text: Callable[[str], str], make_backup: bool
) -> None:
    if make_backup:
        make_bak(filename)
        curr_text = get_as_text(filename)
        original_text = get_original_text(filename)
    else:
        curr_text = original_text = get_as_text(filename)
    filedata = replace_text(original_text)
    if filedata != curr_text:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(filedata)


def replace_file_string(
    filename: PathLike, pattern_replace: Sequence[Tuple[str, str]], make_backup: bool
) -> None:
    def __replace_text(text: str) -> str:
        for pattern, replace in pattern_replace:
            text = re.sub(pattern, replace, text, flags=re.MULTILINE | re.DOTALL)
        return text

    _replace_file_content(filename, __replace_text, make_backup)


def insert_line_after(
    filename: PathLike, insert_after: Mapping[str, str], make_backup: bool
) -> None:
    def __replace_text(text: str) -> str:
        new_lines: List[str] = []
        lines = text.split("\n")
        for line in lines:
            new_lines.append(line)
            if line in insert_after:
                new_lines.append(insert_after[line])
        return "\n".join(new_lines) + "\n"

    _replace_file_content(filename, __replace_text, make_backup)


def call_subprocess(cmd: Sequence[str], show_info: bool = True) -> None:
    try:
        _env: Dict[str, str] = {}
        _env.update(os.environ)
        _CL_env_for_MSVC: Mapping[str, str] = {
            "CL": "/source-charset:utf-8 /execution-charset:utf-8"
        }
        _env.update(_CL_env_for_MSVC)
        logging.info(f"pwd={os.path.abspath(os.curdir)}")

        def __t(text: str) -> str:
            if '"' in text:
                return text
            if " " in text:
                return '"' + text + '"'
            return text

        cmdline = " ".join([__t(s) for s in cmd if s])
        logging.info(cmdline)
        if get_os() == "win":
            subprocess.check_call(cmdline, env=_env)
        else:
            subprocess.check_call(cmd, env=_env)
    except subprocess.CalledProcessError as e:
        logging.warning(e)
        sys.exit(e.returncode)


def remove_if_exist(path: Path):
    if path.exists():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


def makefile_to_lines(filename: PathLike) -> Iterable[str]:
    lines: List[str] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            if line.endswith("\n"):
                line = line[:-1]
            if line.endswith("\\"):
                lines.append(line[:-1])
            else:
                lines.append(line)
                yield re.sub("[ \\t]+", " ", "".join(lines))
                lines = []


def match_and_add(pattern: re.Pattern, dest: List[str], line: str) -> None:
    match = pattern.match(line)
    if match:
        for name in [s.strip() for s in match["name"].split(" ")]:
            if name and name != "$(NULL)":
                dest.append(name)


def get_value_from_env(env: str, default: Optional[str] = None) -> Optional[str]:
    if env not in os.environ:
        return default
    return os.environ[env]


def get_vs_ver() -> VisualStudioVersion:
    env_name = "VisualStudioVersion"
    vs_version = get_value_from_env(env_name)
    if not vs_version:
        raise ValueError(f"{env_name} is empty.")
    if vs_version not in typing.get_args(VisualStudioVersion):
        raise ValueError(f"Unknown Visual Studio version: {vs_version}.")
    return cast(VisualStudioVersion, vs_version)


def get_msvc_internal_ver() -> MSVCInternalVersion:
    return _vs_to_msvc_internal_ver[get_vs_ver()]


def load_msbuild_xml(path: PathLike) -> ElementTree:
    ns = {"msbuild": "http://schemas.microsoft.com/developer/msbuild/2003"}
    ET.register_namespace("", ns["msbuild"])
    tree = ET.parse(path)
    return tree


def load_nuspec_xml(path: PathLike) -> ElementTree:
    ns = {"nuspec": "http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd"}
    ET.register_namespace("", ns["nuspec"])
    tree = ET.parse(path)
    return tree


def get_elems(parent: Element, name: str, ns: Optional[str] = None) -> Iterable[Element]:
    ns_name = name
    if ns is not None:
        ns_name = "{" + ns + "}" + ns_name
    return (e for e in parent if e.tag == ns_name)


def get_elem(parent: Element, name: str, ns: Optional[str] = None) -> Element:
    elms = list(get_elems(parent, name, ns))
    if len(elms) != 1:
        raise RuntimeError(f"Number of <{name}> is {len(elms)}.")
    return elms[0]


class Config:
    def __init__(self):
        self.this_path: Optional[Path] = None
        self.rdkit_path: Optional[Path] = None
        self.boost_path: Optional[Path] = None
        self.eigen_path: Optional[Path] = None
        self.zlib_path: Optional[Path] = None
        self.libpng_path: Optional[Path] = None
        self.pixman_path: Optional[Path] = None
        self.cairo_path: Optional[Path] = None
        self.freetype_path: Optional[Path] = None
        self.minor_version: int = 1
        self.cairo_support: bool = False
        self.freetype_support: bool = False
        self.swig_patch_enabled: bool = True
        self.use_boost: bool = False
        self.test_enabled: bool = False
        self.limit_external: bool = False
        self.use_static_libs: bool = False
        self.target_lang: LangType = LangType.CPlusPlus


def to_on_off(flag: bool) -> str:
    return "ON" if flag else "OFF"


def get_shared_lib_names(binary_path: Path) -> Iterable[str]:
    dependent_dll_names: Set[str] = set()
    if get_os() == "win":
        cmdline = f"dumpbin.exe /DEPENDENTS {binary_path}"
        proc = subprocess.run(cmdline, shell=True, stdout=PIPE, text=True)
        if proc.returncode != 0:
            raise RuntimeError("Failed to execute dumpbin")
        pat = re.compile(" ([a-zA-Z0-9_\\-]+\\.dll) ")
        for name in re.findall(pat, proc.stdout, flags=0):
            dependent_dll_names.add(name)
    elif get_os() == "linux":
        cmdline = f"ldd {binary_path}"
        proc = subprocess.run(cmdline, shell=True, stdout=PIPE, text=True)
        if proc.returncode != 0:
            raise RuntimeError("Failed to execute ldd")
        pat = re.compile(" ([a-zA-Z0-9_\\-]+\\.so\\.\\d+)\\s+\\=\\>")
        for name in re.findall(pat, proc.stdout, flags=0):
            dependent_dll_names.add(name)
    else:
        raise RuntimeError
    return dependent_dll_names


def vcxproj_to_vscurr(proj_file: Path) -> None:
    ns = "http://schemas.microsoft.com/developer/msbuild/2003"
    tree = load_msbuild_xml(proj_file)
    project = tree.getroot()
    for prop_grp in get_elems(project, "PropertyGroup", ns):
        if "Label" in prop_grp.attrib and prop_grp.attrib["Label"] == "Globals":
            vc_proj_ver = get_elem(prop_grp, "VCProjectVersion", ns)
            vc_proj_ver.text = get_vs_ver()
            break
    else:
        raise RuntimeError(f"VCProjectVersion is missing in {proj_file}")

    for prop_grp in get_elems(project, "PropertyGroup", ns):
        for elm in prop_grp:
            if elm.tag == "{" + ns + "}" + "PlatformToolset":
                elm.text = "v" + get_msvc_internal_ver().replace(".", "")

    tree.write(proj_file, "utf-8", True)


class NativeMaker:
    def __init__(self, config: Config, build_platform: Optional[CpuModel] = None):
        self.build_platform: Optional[CpuModel] = build_platform if build_platform else "x64"
        self.config: Config = config

    @property
    def g_option_of_cmake(self) -> Sequence[str]:
        if get_os() == "linux":
            return ["-GUnix Makefiles"]
        if get_os() == "win":
            assert self.build_platform
            return _vs_ver_to_cmake_option_catalog[get_vs_ver()][self.build_platform]
        raise RuntimeError

    @property
    def build_dir_name(self) -> str:
        """Returns build path. Typically "buildx86".

        Returns:
            str: Directory name.
        """
        assert self.build_platform
        return f"build{self.build_platform}"

    @property
    def build_dir_name_of_rdkit(self) -> str:
        """Returns build path for RDKit. Typically "buildx86winCSharp".

        Returns:
            str: Directory name.
        """
        assert self.build_platform
        return f"build{get_os()}{self.build_platform}{_LangType_to_str[self.config.target_lang]}"

    @property
    def ms_build_platform(self) -> MSPlatform:
        assert self.build_platform
        return _platform_to_ms_form[self.build_platform]

    @property
    def address_model(self) -> AddressModel:
        assert self.build_platform
        return _platform_to_address_model[self.build_platform]

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
        return self.boost_path / f"lib{self.address_model}-msvc-{get_msvc_internal_ver()}"

    @property
    def rdkit_build_path(self) -> Path:
        return self.rdkit_path / self.build_dir_name_of_rdkit

    @property
    def rdkit_csharp_wrapper_path(self) -> Path:
        return self.rdkit_path / "Code" / "JavaWrappers" / "csharp_wrapper"

    @property
    def rdkit_swig_csharp_path(self) -> Path:
        return self.rdkit_csharp_wrapper_path / "swig_csharp"

    def get_rdkit_version(self) -> int:
        return int(re.sub(r".*_(\d\d\d\d)_(\d\d)_(\d)", r"\1\2\3", str(self.config.rdkit_path)))

    def get_version_for_nuget(self) -> str:
        return f"0.{self.get_rdkit_version()}.{self.config.minor_version}"

    def get_version_for_rdkit_dotnetwrap(self) -> str:
        num = self.get_rdkit_version()
        major, minor, build, revision = (
            0,
            (num // 10) % 10000,
            num % 10,
            self.config.minor_version,
        )
        return f"{major}.{minor}.{build}.{revision}"

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

    @property
    def zlib_lib_path(self):
        return (
            self.zlib_path
            / self.build_dir_name
            / "Release"
            / ("zlibstatic.lib" if self.config.use_static_libs else "zlib.lib")
        )

    def run_msbuild(self, proj: Union[PathLike, str], platform: Optional[str] = None) -> None:
        if not platform:
            platform = self.ms_build_platform
        cmd = [
            "MSBuild",
            str(proj),
            f"/p:Configuration=Release,Platform={platform}",
            "/maxcpucount",
        ]
        call_subprocess(cmd)

    def make_zlib(self) -> None:
        build_path = self.zlib_path / self.build_dir_name
        build_path.mkdir(exist_ok=True)
        _curdir = os.path.abspath(os.curdir)
        try:
            os.chdir(build_path)
            cmd = ["cmake", str(self.zlib_path)] + list(self.g_option_of_cmake)
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
                ["cmake", str(self.libpng_path)]
                + list(self.g_option_of_cmake)
                + [
                    f'-DZLIB_LIBRARY="{str(self.zlib_lib_path)}"',
                    f'-DZLIB_INCLUDE_DIR="{str(self.zlib_path)}"',
                    f"-DPNG_SHARED={to_on_off(not self.config.use_static_libs)}",
                    f"-DPNG_STATIC={to_on_off(self.config.use_static_libs)}",
                ]
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

            vcxproj_to_vscurr(proj_file)

            makefile_win32 = self.pixman_path / "pixman" / "Makefile.win32"
            makefile_sources = self.pixman_path / "pixman" / "Makefile.sources"

            c_files: List[str] = []
            i_files: List[str] = []

            pattern_c = re.compile("^libpixman_sources\\s*\\=(?P<name>.*)$")
            pattern_h = re.compile("^libpixman_headers\\s*\\=(?P<name>.*)$")
            for line in makefile_to_lines(makefile_sources):
                match_and_add(pattern_c, c_files, line)
                match_and_add(pattern_h, i_files, line)

            pattern_c = re.compile("^\\s*libpixman_sources\\s*\\+\\=(?P<name>.*)$")
            for line in makefile_to_lines(makefile_win32):
                match_and_add(pattern_c, c_files, line)

            tree = load_msbuild_xml(proj_file)
            root = tree.getroot()
            item_group = SubElement(root, "ItemGroup")
            for name in c_files:
                node = SubElement(item_group, "ClCompile")
                node.attrib["Include"] = f"..\\pixman\\{name}"
            for name in i_files:
                node = SubElement(item_group, "ClInclude")
                node.attrib["Include"] = f"..\\pixman\\{name}"

            tree.write(proj_file, "utf-8", True)
            self.run_msbuild(proj_file)
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
            vcxproj_to_vscurr(proj_file)
            replace_file_string(
                proj_file,
                [
                    (
                        "__CAIRODIR__",
                        str(self.cairo_path).replace("\\", "\\\\"),
                    ),
                    (
                        "__LIBPNGDIR__",
                        str(self.libpng_path).replace("\\", "\\\\"),
                    ),
                    (
                        "__ZLIBDIR__",
                        str(self.zlib_path).replace("\\", "\\\\"),
                    ),
                    (
                        "__PIXMANDIR__",
                        str(self.pixman_path).replace("\\", "\\\\"),
                    ),
                    (
                        "__FREETYPEDIR__",
                        str(self.freetype_path).replace("\\", "\\\\"),
                    ),
                ],
                make_backup=False,
            )
            self.run_msbuild(vcxproj)
        finally:
            os.chdir(_curdir)

    def make_freetype(self) -> None:
        _curdir = os.path.abspath(os.curdir)
        try:
            os.chdir(self.freetype_path)
            shutil.copy2(
                self.this_path / "files" / "freetype" / "freetype.vcxproj",
                self.freetype_path / "builds" / "windows" / "vc2010",
            )
            os.chdir(self.freetype_path / "builds" / "windows" / "vc2010")
            logging.debug(f"current dir = {os.getcwd()}")
            self.run_msbuild("freetype.sln")
        finally:
            os.chdir(_curdir)

    @property
    def path_streams_cpp(self) -> Path:
        return self.rdkit_path / "Code" / "RDStreams" / "streams.cpp"

    @property
    def path_streams_h(self) -> Path:
        return self.rdkit_path / "Code" / "RDStreams" / "streams.h"

    @property
    def path_GraphMolCSharp_i(self) -> Path:
        return self.rdkit_csharp_wrapper_path / "GraphMolCSharp.i"

    @property
    def path_Descriptors_i(self) -> Path:
        return self.rdkit_path / "Code" / "JavaWrappers" / "Descriptors.i"

    @property
    def path_MolDescriptors_h(self) -> Path:
        return self.rdkit_path / "Code" / "GraphMol" / "Descriptors" / "MolDescriptors.h"

    @property
    def path_MolSupplier_i(self) -> Path:
        return self.rdkit_path / "Code" / "JavaWrappers" / "MolSupplier.i"

    @property
    def path_Streams_i(self) -> Path:
        return self.rdkit_path / "Code" / "JavaWrappers" / "Streams.i"

    @property
    def path_MolDraw2D_i(self) -> Path:
        return self.rdkit_path / "Code" / "JavaWrappers" / "MolDraw2D.i"

    @property
    def path_MolDraw2D_h(self) -> Path:
        return self.rdkit_path / "Code" / "GraphMol" / "MolDraw2D" / "MolDraw2D.h"

    @property
    def bakable_files(self) -> Iterable[Path]:
        return [
            self.path_streams_cpp,
            self.path_streams_h,
            self.path_GraphMolCSharp_i,
            self.path_Descriptors_i,
            self.path_MolDescriptors_h,
            self.path_MolSupplier_i,
            self.path_Streams_i,
            self.path_MolDraw2D_i,
            self.path_MolDraw2D_h,
        ]

    @property
    def path_RDKit2DotNet_folder(self):
        return self.rdkit_csharp_wrapper_path / "RDKit2DotNet"

    def build_cmake_rdkit(self) -> Sequence[str]:
        self.rdkit_build_path.mkdir(exist_ok=True)
        _curdir = os.path.abspath(os.curdir)
        os.chdir(self.rdkit_build_path)
        try:
            self._patch_i_files()
            cmd = self._make_rdkit_cmake()
            return cmd
        finally:
            os.chdir(_curdir)

    def build_rdkit(self) -> None:
        self.rdkit_build_path.mkdir(exist_ok=True)
        _curdir = os.path.abspath(os.curdir)
        os.chdir(self.rdkit_build_path)
        try:
            if get_os() == "win":
                self.run_msbuild("RDKit.sln")
            else:
                cmd = ["make", "-j"]
                if self.config.target_lang == LangType.CPlusPlus:
                    pass
                elif self.config.target_lang == LangType.CSharp:
                    cmd += ["RDKFuncs"]
                else:
                    raise AssertionError
                call_subprocess(cmd)
        finally:
            os.chdir(_curdir)

    def copy_rdkit_dlls(self) -> None:
        self._copy_dlls()

    def _patch_GraphMolCSharp_i(self):
        dic: Dict[str, str] = dict()
        _line = r"%shared_ptr(RDKit::QueryOps)"
        _insert = r"%shared_ptr(RDKit::MolBundle)" + "\n"
        _insert += r"%shared_ptr(RDKit::FixedMolSizeMolBundle)"
        dic.update({_line: _insert})
        _line = r"%shared_ptr(RDKit::SmilesParseException)"
        _insert = r"%shared_ptr(RDKit::MolPicklerException)"
        dic.update({_line: _insert})
        _line = r'%include "../QueryOps.i"'
        _insert = r'%include "../MolBundle.i"'
        dic.update({_line: _insert})
        _line = r'%include "../Trajectory.i"'
        _insert = r'%include "../MolStandardize.i"'
        dic.update({_line: _insert})
        _line = r'%include "../SubstanceGroup.i"'
        _insert = r'%include "../MolEnumerator.i"'
        dic.update({_line: _insert})
        insert_line_after(self.path_GraphMolCSharp_i, dic, make_backup=True)
        if self.config.swig_patch_enabled and self.get_rdkit_version() < 2021032:
            replace_file_string(
                self.path_GraphMolCSharp_i,
                [("boost::int32_t", "int32_t"), ("boost::uint32_t", "uint32_t")],
                make_backup=False,  # backed up above
            )

    def _patch_MolDraw2D_i(self):
        dic: Dict[str, str] = dict()
        _svg_h = "<GraphMol/MolDraw2D/MolDraw2DSVG.h>"
        _cairo_h = "<GraphMol/MolDraw2D/MolDraw2DCairo.h>"
        _line = f"#include {_svg_h}"
        _insert = f"""
#ifdef RDK_BUILD_CAIRO_SUPPORT
#include {_cairo_h}
#endif
"""
        dic.update({_line: _insert})
        _line = f"%include {_svg_h}"
        _insert = f"""
#ifdef RDK_BUILD_CAIRO_SUPPORT
%include {_cairo_h}
#endif
"""
        dic.update({_line: _insert})
        _line = "%template(Int_Vect_Vect) std::vector<std::vector<int> >;"
        _insert = """
%template(UInt_Vect_Vect) std::vector<std::vector<unsigned int> >;
%template(Double_Vect_Vect) std::vector<std::vector<double> >;
%template(Point3D_Const_Vect) std::vector<const RDGeom::Point3D *>;
%template(Point3D_Val_Vect) std::vector<RDGeom::Point3D>;
"""
        insert_line_after(self.path_MolDraw2D_i, dic, make_backup=True)

    def _patch_MolDraw2D_h(self) -> None:
        dic: Dict[str, str] = dict()
        _line = r"  const MolDrawOptions &drawOptions() const { return options_; }"
        _insert = (
            r"void setDrawOptions(const RDKit::MolDrawOptions &opts) { drawOptions() = opts; }"
        )
        dic.update({_line: _insert})
        insert_line_after(self.path_MolDraw2D_h, dic, make_backup=True)

    def _patch_MolDescriptors_h(self) -> None:
        dic: Dict[str, str] = dict()
        _line = r"SET(CMAKE_SWIG_OUTDIR ${CMAKE_CURRENT_SOURCE_DIR}/swig_csharp )"
        _insert = r"""
if(RDK_BUILD_DESCRIPTORS3D)
SET(CMAKE_SWIG_FLAGS "-DRDK_BUILD_DESCRIPTORS3D" "-DRDK_HAS_EIGEN3" ${CMAKE_SWIG_FLAGS} )
endif()
if(RDK_BUILD_CAIRO_SUPPORT)
SET(CMAKE_SWIG_FLAGS "-DRDK_BUILD_CAIRO_SUPPORT" ${CMAKE_SWIG_FLAGS} )
endif()
"""
        dic.update({_line: _insert})
        path = self.rdkit_path / "Code" / "JavaWrappers" / "csharp_wrapper" / "CMakeLists.txt"
        insert_line_after(path, dic, make_backup=True)

        _line = r"#include <GraphMol/Descriptors/MolDescriptors.h>"
        _insert = """
#include <GraphMol/Descriptors/AtomFeat.h>
#include <GraphMol/Descriptors/USRDescriptor.h>
#include <GraphMol/Depictor/RDDepictor.h>
#ifdef RDK_BUILD_DESCRIPTORS3D
#include <GraphMol/Descriptors/MolDescriptors3D.h>
#endif
"""
        dic.update({_line: _insert})
        _line = r"%include <GraphMol/Descriptors/MQN.h>"
        _insert = """
%include <GraphMol/Descriptors/AUTOCORR2D.h>
%include <GraphMol/Descriptors/AtomFeat.h>
%include <GraphMol/Descriptors/USRDescriptor.h>
%include <GraphMol/Depictor/RDDepictor.h>
#ifdef RDK_HAS_EIGEN3
%include <GraphMol/Descriptors/BCUT.h>
#endif
#ifdef RDK_BUILD_DESCRIPTORS3D
%include <GraphMol/Descriptors/CoulombMat.h>
%include <GraphMol/Descriptors/EEM.h>
%include <GraphMol/Descriptors/PBF.h>
%include <GraphMol/Descriptors/RDF.h>
%include <GraphMol/Descriptors/MORSE.h>
%include <GraphMol/Descriptors/WHIM.h>
%include <GraphMol/Descriptors/GETAWAY.h>
%include <GraphMol/Descriptors/AUTOCORR3D.h>
%include <GraphMol/Descriptors/PMI.h>
#endif
"""
        dic.update({_line: _insert})
        insert_line_after(self.path_Descriptors_i, dic, make_backup=True)
        dic = dict()
        _line = "#include <GraphMol/Descriptors/MQN.h>"
        _insert = "#include <GraphMol/Descriptors/BCUT.h>"
        dic.update({_line: _insert})
        insert_line_after(self.path_MolDescriptors_h, dic, make_backup=True)

    def _patch_MolSupplier_i(self):
        __t0 = "%extend RDKit::ForwardSDMolSupplier {\n"
        __t1 = "};\n"
        replace_file_string(
            self.path_MolSupplier_i,
            [
                (__t0, "#ifdef RDK_USE_BOOST_IOSTREAMS\n" + __t0),
                (__t1, __t1 + "#endif\n"),
            ],
            make_backup=True,
        )

    def _patch_Streams_i(self):
        __t2 = "%extend RDKit::gzstream {\n"
        __t3 = "%include <../RDStreams/streams.h>"
        replace_file_string(
            self.path_Streams_i,
            [
                (__t2, "#ifdef RDK_USE_BOOST_IOSTREAMS\n" + __t2),
                (__t3, "#endif\n" + __t3),
            ],
            make_backup=True,
        )

    def _patch_i_files(self):
        self._patch_GraphMolCSharp_i()
        self._patch_MolDraw2D_i()
        self._patch_MolDraw2D_h()
        self._patch_MolDescriptors_h()
        self._patch_MolSupplier_i()
        self._patch_Streams_i()

    def _make_rdkit_cmake(self) -> Sequence[str]:
        cmd: List[str] = self._get_cmake_rdkit_cmd_line()
        if get_os() == "win":
            cmd = [a.replace("\\", "/") for a in cmd]
        call_subprocess(cmd)
        return cmd

    def _get_cmake_rdkit_cmd_line(self) -> List[str]:
        def f_test() -> str:
            return to_on_off(self.config.test_enabled)

        def f_boost() -> str:
            return to_on_off(self.config.use_boost)

        def f_no_limit_external() -> str:
            return to_on_off(not self.config.limit_external)

        args = [f"{str(self.rdkit_path)}"]
        args += ["-Wdev"]
        args += self.g_option_of_cmake
        if self.config.target_lang == LangType.CPlusPlus:
            args += [
                "-DRDK_BUILD_SWIG_WRAPPERS=OFF",
                "-DRDK_BUILD_SWIG_CSHARP_WRAPPER=OFF",
                "-DRDK_BUILD_SWIG_JAVA_WRAPPER=OFF",
                "-DRDK_BUILD_PYTHON_WRAPPERS=OFF",
            ]
        elif self.config.target_lang == LangType.CSharp:
            args += [
                "-DRDK_BUILD_SWIG_WRAPPERS=ON",
                "-DRDK_BUILD_SWIG_CSHARP_WRAPPER=ON",
                "-DRDK_BUILD_SWIG_JAVA_WRAPPER=OFF",
                "-DRDK_BUILD_PYTHON_WRAPPERS=OFF",
            ]
        else:
            raise RuntimeError(f"Not supported. {self.config.target_lang}")
        if self.config.boost_path:
            args += [
                f"-DBOOST_ROOT={str(self.boost_path)}",
                f"-DBOOST_INCLUDEDIR={str(self.boost_path)}",
                f"-DBOOST_LIBRARYDIR={str(self.boost_bin_path)}",
            ]
        if self.config.eigen_path:
            args += [f"-DEIGEN3_INCLUDE_DIR={str(self.eigen_path)}"]
        if self.config.zlib_path:
            zlib_lib_path = (
                self.zlib_path
                / self.build_dir_name
                / "Release"
                / ("zlibstatic.lib" if self.config.use_static_libs else "zlib.lib")
            )
            args += [
                f'-DZLIB_LIBRARIES="{zlib_lib_path}"',
                f'-DZLIB_INCLUDE_DIRS="{self.zlib_path}"',
            ]
        if self.config.cairo_support:
            if self.config.cairo_path:
                cairo_lib_path = (
                    self.cairo_path / "vc2017" / self.ms_build_platform / "Release" / "cairo.lib"
                )
                args += [
                    f'-DCAIRO_INCLUDE_DIRS={self.cairo_path / "src"}',
                    f"-DCAIRO_LIBRARIES={cairo_lib_path}",
                ]
        args += [
            "-DRDK_INSTALL_INTREE=ON",
            f"-DRDK_BUILD_CPP_TESTS={f_test()}",
            f"-DRDK_USE_BOOST_SERIALIZATION={f_boost()}",
            f"-DRDK_USE_BOOST_IOSTREAMS={f_boost()}",
            f"-DRDK_USE_BOOST_REGEX={f_boost()}",
            "-DBoost_NO_BOOST_CMAKE=ON",
            f"-DRDK_BUILD_COORDGEN_SUPPORT={f_no_limit_external()}",
            f"-DRDK_BUILD_MAEPARSER_SUPPORT={f_no_limit_external()}",
            "-DRDK_OPTIMIZE_POPCNT=ON",
            f"-DRDK_BUILD_FREESASA_SUPPORT={f_no_limit_external()}",
            f"-DRDK_BUILD_CAIRO_SUPPORT={to_on_off(self.config.cairo_support)}",
            f"-DRDK_BUILD_FREETYPE_SUPPORT={to_on_off(self.config.cairo_support)}",
            "-DRDK_BUILD_THREADSAFE_SSS=ON",
            f"-DRDK_BUILD_INCHI_SUPPORT={f_no_limit_external()}",
            f"-DRDK_BUILD_AVALON_SUPPORT={f_no_limit_external()}",
            # do not install comic fonts because of incorrect md5 checksum.
            # see https://salsa.debian.org/debichem-team/rdkit/-/commit/15da2bc1796c507e0c3afa36eecfc1961d16c13e  # NOQA
            "-DRDK_INSTALL_COMIC_FONTS=OFF",
            f"-DRDK_BUILD_TEST_GZIP={f_test()}",
        ]

        if self.get_rdkit_version() >= 2020091:
            # needs followings after 2020_09_1
            args += [
                "-DRDK_USE_URF=ON",
            ]
            if get_os() == "win":
                if self.config.use_static_libs:
                    args += [
                        "-DRDK_SWIG_STATIC=ON",
                        "-DRDK_INSTALL_STATIC_LIBS=ON",
                        "-DBOOST_USE_STATIC_LIBS=ON",
                        "-DRDL_WIN_STATIC=ON",
                    ]
                else:
                    args += [
                        "-DRDK_SWIG_STATIC=OFF",
                        "-DRDK_INSTALL_STATIC_LIBS=OFF",
                        "-DRDK_INSTALL_DLLS_MSVC=ON",
                    ]
            if get_os() == "linux":
                if self.config.use_static_libs:
                    args += [
                        "-DRDK_SWIG_STATIC=ON",
                        "-DRDK_INSTALL_STATIC_LIBS=ON",
                        "-DBOOST_LIBRARYDIR=/usr/lib/x86_64-linux-gnu",
                        "-DBOOST_ROOT=/usr",
                        "-DBOOST_USE_STATIC_LIBS=ON",
                    ]
                else:
                    args += [
                        "-DRDK_SWIG_STATIC=OFF",
                        "-DRDK_INSTALL_STATIC_LIBS=OFF",
                    ]
        if self.get_rdkit_version() >= 2020091:
            # freetype supports starts from 2020_09_1
            if self.config.freetype_path:
                freetype_lib_path = (
                    self.freetype_path
                    / "objs"
                    / self.ms_build_platform
                    / "Release"
                    / "freetype.lib"
                )
                freetype_include_path = self.freetype_path / "include"
                args += [
                    f"-DFREETYPE_LIBRARY={freetype_lib_path}",
                    f"-DFREETYPE_INCLUDE_DIRS={freetype_include_path}",
                ]
        return ["cmake"] + args

    def get_RDKFuncs_dll_path(self) -> Path:
        a: Path
        a = self.rdkit_build_path / "Code" / "JavaWrappers" / "csharp_wrapper"
        if get_os() == "win":
            a = a / "Release" / "RDKFuncs.dll"
        elif get_os() == "linux":
            a = a / "RDKFuncs.so"
        else:
            raise RuntimeError
        return a

    def _copy_dlls(self) -> None:
        assert self.build_platform
        dll_dest_path = self.rdkit_csharp_wrapper_path / get_os() / self.build_platform
        remove_if_exist(dll_dest_path)
        os.makedirs(dll_dest_path)
        logging.info(f"Copy DLLs to {dll_dest_path}.")

        files_to_copy: List[Union[str, PathLike]] = []

        if self.config.target_lang == LangType.CSharp:
            files_to_copy.append(self.get_RDKFuncs_dll_path())

        # pick up dependent DLLs in buildlinux*CSharp/lib or buildwin*CSharp\bin\Release
        if get_os() == "win":
            lib_path = self.rdkit_build_path / "bin" / "Release"
            for file_path in lib_path.glob("*.dll"):
                files_to_copy.append(file_path)
        elif get_os() == "linux":
            lib_path = self.rdkit_build_path / "lib"
            for file_path in lib_path.glob("*.so.1"):
                files_to_copy.append(file_path)
        else:
            raise RuntimeError

        if not self.config.use_static_libs:
            if get_os() == "win":
                files_to_copy.append(self.zlib_path / self.build_dir_name / "Release" / "zlib.dll")

                # Pick BOOST Dlls
                if self.config.use_boost:
                    # DLLs of boost.
                    for file_path in self.boost_bin_path.glob("*.dll"):
                        if re.match(r".*\-vc\d\d\d\-mt\-x(32|64)\-\d_\d\d\.dll", file_path.name):
                            # boost_python-vc###-mt-x##-#_##.dll is not needed.
                            if file_path.name.startswith("boost_python"):
                                continue
                            files_to_copy.append(file_path)

                # DLLs of freetype.
                if self.config.freetype_support and self.get_rdkit_version() >= 2020091:
                    files_to_copy.append(
                        self.freetype_path
                        / "objs"
                        / self.ms_build_platform
                        / "Release"
                        / "freetype.dll"
                    )

                # DLLs of cairo.
                if self.config.cairo_support:
                    files_to_copy += [
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

        # Copy files.
        for path in files_to_copy:
            shutil.copy2(path, dll_dest_path)

    def build_csharp_wrapper(self) -> None:
        self._patch_rdkit_swig_created_files()
        self._prepare_RDKitDotNet_folder()
        self._copy_test_projects()
        self._build_RDKit2DotNet()

    def _patch_rdkit_swig_created_files(self) -> None:
        # Customize the followings if required.
        if self.config.swig_patch_enabled:
            swig_patches: List[Tuple[Path, Sequence[Tuple[str, str]]]] = []
            if self.get_rdkit_version() < 2021032:
                swig_patches += [
                    (
                        # extract BOOST_BINARY.
                        self.rdkit_swig_csharp_path / "PropertyPickleOptions.cs",
                        [("BOOST_BINARY\\(\\s*([01]+)\\s*\\)", "0b\\1")],
                    ),
                    (
                        # remove dupulicated methods.
                        self.rdkit_swig_csharp_path / "RDKFuncs.cs",
                        [
                            (
                                "public static double DiceSimilarity\\([^\\}]*\\."
                                "DiceSimilarity__SWIG_(12|13|14)\\([^\\}]*\\}",
                                "",
                            )
                        ],
                    ),
                ]
            swig_patches += [
                (
                    self.rdkit_swig_csharp_path / "CXSmilesFields.cs",
                    [
                        (
                            "std\\:\\:numeric_limits\\<\\s*std\\:\\:int32_t\\s*\\>\\:\\:max\\(\\)",
                            "0x7fffffff",
                        )
                    ],
                )
            ]
            for filepath, patterns in swig_patches:
                replace_file_string(filepath, patterns, make_backup=False)

        for filepath, patterns in (
            (
                self.rdkit_swig_csharp_path / "RDKFuncsPINVOKE.cs",
                [("(partial )?class RDKFuncsPINVOKE\\s*\\{", "partial class RDKFuncsPINVOKE {")],
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
            replace_file_string(filepath, patterns, make_backup=False)
        shutil.copy2(
            self.this_path / "files" / "rdkit" / "RDKFuncsPINVOKE_Loader.cs",
            self.rdkit_swig_csharp_path,
        )

    def _prepare_RDKitDotNet_folder(self):
        remove_if_exist(self.path_RDKit2DotNet_folder)
        shutil.copytree(
            self.this_path / "files" / "rdkit" / "RDKit2DotNet",
            self.rdkit_csharp_wrapper_path / "RDKit2DotNet",
        )
        path_RDKit2DotNet_csproj = self.path_RDKit2DotNet_folder / "RDKit2DotNet.csproj"
        rdkit_dotnetwrap_version = self.get_version_for_rdkit_dotnetwrap()
        tree = load_msbuild_xml(path_RDKit2DotNet_csproj)
        project = tree.getroot()
        prop_grp = list(get_elems(project, "PropertyGroup"))[0]
        asm_ver = get_elem(prop_grp, "AssemblyVersion")
        asm_ver.text = rdkit_dotnetwrap_version
        file_ver = get_elem(prop_grp, "FileVersion")
        file_ver.text = rdkit_dotnetwrap_version
        property_group = SubElement(project, "PropertyGroup")
        sign_assembly = SubElement(property_group, "SignAssembly")
        sign_assembly.text = "true"
        assembly_originator_key_file = SubElement(property_group, "AssemblyOriginatorKeyFile")
        assembly_originator_key_file.text = "rdkit2dotnet.snk"

        # below is only for convenience to run test project
        item_group = SubElement(project, "ItemGroup")
        for cpu_model in typing.get_args(CpuModel):
            for filename in glob.glob(
                str(self.rdkit_csharp_wrapper_path / get_os() / cpu_model / "*.dll")
            ):
                dllbasename = os.path.basename(filename)
                content = SubElement(item_group, "None")
                path_to_dll = f"..\\\\{get_os()}\\\\{cpu_model}\\\\{dllbasename}"
                link_to_dll = f"runtimes\\\\{get_os()}-{cpu_model}\\\\native\\\\{dllbasename}"
                content.attrib["Include"] = path_to_dll
                content.attrib["Link"] = link_to_dll
                copy_to_output_directory = SubElement(content, "CopyToOutputDirectory")
                copy_to_output_directory.text = "PreserveNewest"
        tree.write(path_RDKit2DotNet_csproj, "utf-8", True)

    @property
    def test_csprojects(self) -> Collection[str]:
        return (
            "RDKit2DotNetTest",
            "RDKit2DotNetTest2",
            "NuGetExample",
            "NuGetExample2",
        )

    @property
    def test_sln_names(self) -> Collection[str]:
        return (
            "RDKit2DotNet.sln",
            "NuGetExample.sln",
        )

    def _copy_test_projects(self) -> None:
        path_rdkit_files = self.this_path / "files" / "rdkit"
        for name in self.test_csprojects:
            remove_if_exist(self.rdkit_csharp_wrapper_path / name)
            shutil.copytree(
                path_rdkit_files / name,
                self.rdkit_csharp_wrapper_path / name,
                dirs_exist_ok=True,
            )
            proj_path = self.rdkit_csharp_wrapper_path / name / f"{name}.csproj"
            tree = load_msbuild_xml(proj_path)
            project = tree.getroot()
            for item_grp in get_elems(project, "ItemGroup"):
                for pkg_ref in get_elems(item_grp, "PackageReference"):
                    if (
                        "Include" in pkg_ref.attrib
                        and pkg_ref.attrib["Include"] == "RDKit.DotNetWrap"
                    ):
                        pkg_ref.attrib["Version"] = self.get_version_for_nuget()
            tree.write(proj_path, "utf-8", True)
        for name in self.test_sln_names:
            shutil.copy2(path_rdkit_files / name, self.rdkit_csharp_wrapper_path)
        print(f"Test slns {self.test_sln_names} are created in {self.rdkit_csharp_wrapper_path}.")
        print("RDKit2DotNetTest: .NET 5.0 example.")
        print("RDKit2DotNetTest2: .NET Framework 4 example.")
        print("NuGetExample: NuGet package example for .NET 5.0.")
        print("NuGetExample2: NuGet package example for .NET Framework 4.")

    def _build_RDKit2DotNet(self) -> None:
        _pushd_build_wrapper = os.getcwd()
        try:
            os.chdir(self.path_RDKit2DotNet_folder)
            call_subprocess(["dotnet", "restore"])
            call_subprocess(
                ["dotnet", "build", "RDKit2DotNet.csproj", "/t:Build", "/p:Configuration=Release"]
            )
        finally:
            os.chdir(_pushd_build_wrapper)

    def build_nuget_package(self) -> None:
        dll_basenames_dic = self._make_dll_basenames_dic()
        self._prepare_nuspec_file(dll_basenames_dic)
        self._prepare_targets_file(dll_basenames_dic)
        self._build_nupkg()

    def _make_dll_basenames_dic(self) -> Mapping[str, Mapping[str, Sequence[str]]]:
        dll_basenames_dic: Dict[str, Dict[str, List[str]]] = dict()
        for _os in typing.get_args(SupportedSystem):
            if _os not in dll_basenames_dic:
                dll_basenames_dic[_os] = dict()
            for cpu_model in typing.get_args(CpuModel):
                dlls_path = self.rdkit_csharp_wrapper_path / _os / cpu_model
                dll_basenames: List[str] = []
                for filename in glob.glob(str(dlls_path / "*.*")):
                    dll_basenames.append(os.path.basename(filename))
                dll_basenames_dic[_os][cpu_model] = dll_basenames
        if get_os() == "win":
            assert dll_basenames_dic["win"]["x86"]
            assert dll_basenames_dic["win"]["x64"]
        if get_os() == "linux":
            assert dll_basenames_dic["linux"]["x64"]
            assert not dll_basenames_dic["linux"]["x86"]
        return dll_basenames_dic

    def get_description_for_nuget(self) -> str:
        s = f".NET binding of RDKit Release_{self.get_version_for_rdkit()}."
        if get_os() == "linux":
            s += " Supports Linux (x64)."
        else:
            s += " Supports Windows (x86 and x64) and Linux (x64)."
        return s

    def get_lib_versios(self) -> Sequence[str]:
        lib_versions: List[str] = []
        lib_versions.append(f"Eigen {self.get_version_for_eigen()}")
        if get_os() == "win":
            lib_versions.append(f"zlib {self.get_version_for_zlib()}")
            if self.config.use_boost:
                lib_versions.append(f"Boost {self.get_version_for_boost()}")
            if self.config.freetype_support:
                lib_versions.append(f"FreeType {self.get_version_for_freetype()}")
            if self.config.cairo_support:
                lib_versions += [
                    f"libpng {self.get_version_for_libpng()}",
                    f"pixman {self.get_version_for_pixman()}",
                    f"cairo {self.get_version_for_cairo()}",
                ]
        return lib_versions

    def get_releaseNotes(self) -> str:
        s: str = "This release uses "
        s += ", ".join(self.get_lib_versios())
        if get_os() != "win":
            s += f" built using Visual Studio {self.get_version_for_rdkit()}"
            s += " for Windows build"
        s += "."
        return s

    def _prepare_nuspec_file(
        self, dll_basenames_dic: Mapping[str, Mapping[str, Sequence[str]]]
    ) -> None:
        origin_file = self.this_path / "files" / "rdkit" / f"{project_name}.nuspec"
        nuspec_file = shutil.copy2(origin_file, self.rdkit_csharp_wrapper_path / "RDKit2DotNet")

        tree: ElementTree = load_nuspec_xml(nuspec_file)
        root = tree.getroot()
        ns = "http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd"

        metadata = get_elem(root, "metadata", ns)
        description = get_elem(metadata, "description", ns)
        description.text = self.get_description_for_nuget()
        version = get_elem(metadata, "version", ns)
        version.text = self.get_version_for_nuget()
        releaseNotes = get_elem(metadata, "releaseNotes", ns)
        releaseNotes.text = self.get_releaseNotes()

        files = get_elem(root, "files", ns)
        for _os in typing.get_args(SupportedSystem):
            for cpu_model in typing.get_args(CpuModel):
                for dll_basename in dll_basenames_dic[_os][cpu_model]:
                    file_element = SubElement(files, "file")
                    file_element.attrib["src"] = f"../{_os}/{cpu_model}/{dll_basename}"
                    file_element.attrib[
                        "target"
                    ] = f"runtimes/{_os}-{cpu_model}/native/{dll_basename}"

        tree.write(nuspec_file, "utf-8", True)

    def _prepare_targets_file(
        self, dll_basenames_dic: Mapping[str, Mapping[str, Sequence[str]]]
    ) -> None:
        origin_file = self.this_path / "files" / "rdkit" / f"{project_name}.targets"
        targets_file = shutil.copy2(origin_file, self.rdkit_csharp_wrapper_path / "RDKit2DotNet")

        tree: ElementTree = load_msbuild_xml(targets_file)
        project = tree.getroot()

        non_net = (
            "!$(TargetFramework.Contains('netstandard')) "
            "And !$(TargetFramework.Contains('netcoreapp')) "
            "And !$(TargetFramework.Contains('net5.'))"
            "And !$(TargetFramework.Contains('net6.'))"
        )
        _os = "win"
        ig: Element
        for cpu_model in typing.get_args(CpuModel):
            ig = SubElement(project, "ItemGroup")
            ig.attrib["Condition"] = f"{non_net} And '$(Platform)' == '{cpu_model}'"
            for dllname in dll_basenames_dic[_os][cpu_model]:
                none = SubElement(ig, "None")
                none.attrib[
                    "Include"
                ] = f"$(MSBuildThisFileDirectory)../runtimes/{_os}-{cpu_model}/native/{dllname}"
                link = SubElement(none, "Link")
                link.text = dllname
                copy_to = SubElement(none, "CopyToOutputDirectory")
                copy_to.text = "PreserveNewest"
        ig = SubElement(project, "ItemGroup")
        ig.attrib["Condition"] = f"{non_net} And '$(Platform)' == 'AnyCPU'"
        _os = "win"
        for cpu_model in typing.get_args(CpuModel):
            for dllname in dll_basenames_dic[_os][cpu_model]:
                none = SubElement(ig, "None")
                none.attrib[
                    "Include"
                ] = f"$(MSBuildThisFileDirectory)../runtimes/{_os}-{cpu_model}/native/{dllname}"
                link = SubElement(none, "Link")
                link.text = f"runtimes/{_os}-{cpu_model}/native/{dllname}"
                copy_to = SubElement(none, "CopyToOutputDirectory")
                copy_to.text = "PreserveNewest"

        tree.write(targets_file, "utf-8", True)

    def _build_nupkg(self) -> None:
        _curr_dir = os.curdir
        os.chdir(self.rdkit_csharp_wrapper_path / "RDKit2DotNet")
        try:
            cmd = [
                "dotnet",
                "pack",
                "RDKit2DotNet.csproj",
                f"-p:NuspecFile={project_name}.nuspec",
                "/p:Configuration=Release",
            ]
            call_subprocess(cmd)
        finally:
            os.chdir(_curr_dir)

    def clean_zlib(self) -> None:
        if self.config.zlib_path:
            for p in typing.get_args(CpuModel):
                remove_if_exist(self.zlib_path / "zconf.h")
                remove_if_exist(self.zlib_path / f"build{p}")

    def clean_rdkit(self) -> None:
        if self.config.rdkit_path:
            for path in self.bakable_files:
                restore_from_bak(path)
            for p in (
                [
                    f"{project_name}.nuspec",
                    f"{project_name}.targets",
                    "swig_csharp",
                    "Properties",
                    "packages",
                ]
                + list(typing.get_args(SupportedSystem))
                + list(self.test_csprojects)
                + list(self.test_sln_names)
            ):
                remove_if_exist(self.rdkit_csharp_wrapper_path / p)
            remove_if_exist(self.rdkit_path / "lib")
            for _os in typing.get_args(SupportedSystem):
                for p in typing.get_args(CpuModel):
                    remove_if_exist(self.rdkit_path / f"build{_os}{p}CSharp")

    def clean(self) -> None:
        self.clean_rdkit()
        if self.config.freetype_path:
            for __cpu_model in typing.get_args(CpuModel):
                remove_if_exist(self.freetype_path / "objs" / _platform_to_ms_form[__cpu_model])
        self.clean_zlib()
        if self.config.libpng_path:
            for p in typing.get_args(CpuModel):
                remove_if_exist(self.libpng_path / f"build{p}")
        if self.config.pixman_path:
            remove_if_exist(self.pixman_path / "vc2017")
        if self.config.cairo_path:
            remove_if_exist(self.cairo_path / "vc2017")


def config_file_to_map(path: Path) -> Mapping[str, str]:
    dic: Dict[str, str] = dict()
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            splitted_line = line.split("=")
            if len(splitted_line) == 0:
                continue
            if len(splitted_line) != 2:
                raise RuntimeError(f"Invalid: {line} in {path}")
            dic[splitted_line[0]] = splitted_line[1]
    return dic


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--build_platform", default="all", choices=list(typing.get_args(CpuModel)) + ["all"]
    )
    parser.add_argument(
        "--target_lang", default="csharp", choices=("csharp", "java", "cpp")
    )
    for opt in (
        "build_zlib",
        "build_libpng",
        "build_pixman",
        "build_freetype",
        "build_cairo",
        "build_rdkit",
        "build_wrapper",
        "build_nuget",
        "build_cmake",
        "disable_swig_patch",
        "use_boost",
        "limit_external",
        "no_cairo",
        "no_freetype",
        "use_static_libs",
        "clean",
        "clean_zlib",
        "clean_rdkit",
        "build_rdkit_only",
        "show_cmake",
        "enable_test",
    ):
        parser.add_argument(f"--{opt}", default=False, action="store_true")
    args = parser.parse_args()

    # x86 is supported only for Windows
    if get_os() == "linux" and args.build_platform == "x86":
        raise RuntimeError("x86 is not supported for Linux system.")
    if get_os() == "linux" and (args.build_platform == "all" or not args.build_platform):
        args.build_platform = "x64"

    default_config: Mapping[str, str] = config_file_to_map(Path("config.txt"))
    config = create_config(args, default_config)
    if args.target_lang == "csharp":
        config.target_lang = LangType.CSharp
    if args.target_lang == "cpp":
        config.target_lang = LangType.CPlusPlus

    config.test_enabled = args.enable_test

    curr_dir = os.getcwd()
    try:
        if args.clean:
            NativeMaker(config).clean()
        else:
            if args.clean_zlib:
                NativeMaker(config).clean_zlib()
            if args.clean_rdkit:
                NativeMaker(config).clean_rdkit()

        for cpu_model in (
            typing.get_args(CpuModel) if args.build_platform == "all" else [args.build_platform]
        ):
            maker = NativeMaker(config, cpu_model)
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
            if args.show_cmake:
                cmd = maker.build_cmake_rdkit()
                print(" ".join([(('"' + s + '"') if (" " in s or '"' in s) else s) for s in cmd]))
            if args.build_cmake:
                maker.build_cmake_rdkit()
            if args.build_rdkit_only:
                maker.build_rdkit()
                maker.copy_rdkit_dlls()
            if args.build_rdkit:
                maker.build_cmake_rdkit()
                maker.build_rdkit()
                maker.copy_rdkit_dlls()
        # if required x64 is used as platform
        maker = NativeMaker(config)
        if args.build_wrapper:
            maker.build_csharp_wrapper()
        if args.build_nuget:
            maker.build_nuget_package()
    finally:
        os.chdir(curr_dir)


def create_config(args: argparse.Namespace, config_info: Mapping[str, str]) -> Config:
    def get_value(env: str) -> Optional[str]:
        value: Optional[str]
        if env in config_info:
            value = config_info[env]
        else:
            value = get_value_from_env(env)
        return value

    def path_from_ini(env: str) -> Optional[Path]:
        value: Optional[str] = get_value(env)
        if value is None:
            return None
        path = Path(value)
        if not path.is_absolute():
            path = here / value
        return path

    def int_from_int(env: str, default: int) -> int:
        value: Optional[str] = get_value(env)
        if value is None:
            return default
        return int(value)

    config = Config()
    config.minor_version = int_from_int("MINOR_VERSION", 1)
    config.swig_patch_enabled = not args.disable_swig_patch
    config.use_boost = args.use_boost
    config.cairo_support = not args.no_cairo
    config.freetype_support = not args.no_freetype
    config.limit_external = args.limit_external
    if config.limit_external:
        config.cairo_support = False
        config.freetype_support = False
    config.this_path = here
    config.use_static_libs = args.use_static_libs
    config.rdkit_path = path_from_ini("RDKIT_DIR")
    if get_os() == "win":
        # These pathes are only for Windows.
        config.boost_path = path_from_ini("BOOST_DIR")
        config.zlib_path = path_from_ini("ZLIB_DIR")
        config.libpng_path = path_from_ini("LIBPNG_DIR")
        config.pixman_path = path_from_ini("PIXMAN_DIR")
        config.freetype_path = path_from_ini("FREETYPE_DIR")
        config.cairo_path = path_from_ini("CAIRO_DIR")
    config.eigen_path = path_from_ini("EIGEN_DIR")
    config.test_enabled = False
    return config


if __name__ == "__main__":
    main()
