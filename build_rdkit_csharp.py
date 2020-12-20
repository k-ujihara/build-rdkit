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
from pathlib import Path
from typing import Any, Dict, List, Mapping, NamedTuple, Optional, Sequence, cast

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
        _CL_env_for_MSVC: Mapping[str, str] = { "CL": "/source-charset:utf-8 /execution-charset:utf-8 /W3" }
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
    swig_path: Optional[Path] = None
    freetype_path: Optional[Path] = None
    number_of_processors: int = 1
    minor_version: int = 1
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
        return f"build{self.build_platform}"

    @property
    def build_dir_name_for_csharp(self) -> str:
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
    def freetype_path(self) -> Path:
        assert self.config.freetype_path
        return self.config.freetype_path

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

    def get_version_for_boost(self) -> str:
        return re.sub(r".*(\d+_\d+_\d+)", r"\1", str(self.config.boost_path))

    def get_version_for_eigen(self) -> str:
        return re.sub(r".*(\d+\.\d+\.\d+)", r"\1", str(self.config.eigen_path))

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
            + "-DRDK_BUILD_CAIRO_SUPPORT=OFF "
            + "-DRDK_BUILD_THREADSAFE_SSS=ON "
            + "-DRDK_BUILD_INCHI_SUPPORT=ON "
            + "-DRDK_BUILD_AVALON_SUPPORT=ON "
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
        cmd = f"MSBuild RDKit.sln /p:Configuration=Release,Platform={self.ms_build_platform} /maxcpucount"
        call_subprocess(cmd)

    def _copy_to_csharp_wrapper(self) -> None:
        assert self.build_platform
        dll_dest_path = self.rdkit_csharp_wrapper_path / self.build_platform
        remove_if_exist(dll_dest_path)
        dll_dest_path.mkdir()
        logging.info(f"Copy DLLs to {dll_dest_path}.")

        # copy "RDKFuncs.dll"
        shutil.copy2(
            self.rdkit_csharp_build_path
            / "Code"
            / "JavaWrappers"
            / "csharp_wrapper"
            / "Release"
            / "RDKFuncs.dll",
            dll_dest_path,
        )
        # copy rdkit dlls
        if self.get_rdkit_version() >= 2020091:
            for filename in glob.glob(
                str(self.rdkit_csharp_build_path / "bin" / "Release" / "*.dll")
            ):
                shutil.copy2(filename, dll_dest_path)

        # copy boost dlls
        for filename in glob.glob(
            str(self.boost_path / f"lib{self.address_model}-msvc-14.1" / "*.dll")
        ):
            if re.match(
                r".*\-vc141\-mt\-x(32|64)\-\d_\d\d\.dll", filename
            ) and not os.path.basename(filename).startswith("boost_python"):
                shutil.copy2(filename, dll_dest_path)

        # copy fonttype
        if self.get_rdkit_version() >= 2020091:
            assert self.freetype_path
            for filename in glob.glob(
                str(
                    self.freetype_path
                    / "objs"
                    / self.ms_build_platform
                    / "Release"
                    / "*.dll"
                )
            ):
                shutil.copy2(filename, dll_dest_path)

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

    def make_freetype(self) -> None:
        _curdir = os.curdir
        try:
            os.chdir(self.freetype_path)
            shutil.copy2(
                self.this_path / "files" / "freetype.vcxproj",
                self.freetype_path / "builds" / "windows" / "vc2010",
            )
            os.chdir(self.freetype_path / "builds" / "windows" / "vc2010")
            logging.debug(f"current dir = {os.getcwd()}")
            cmd = f"MSBuild freetype.sln /p:Configuration=Release,Platform={self.ms_build_platform} /maxcpucount"
            call_subprocess(cmd)
        finally:
            os.chdir(_curdir)

    def build_rdkit(self) -> None:
        self.rdkit_csharp_build_path.mkdir(exist_ok=True)
        _curdir = os.curdir
        os.chdir(self.rdkit_csharp_build_path)
        try:
            if self.config.swig_patch_enabled:
                replace_file_string(
                    self.rdkit_csharp_wrapper_path / "GraphMolCSharp.i",
                    [("boost::int32_t", "int32_t"), ("boost::uint32_t", "uint32_t")],
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
            cmd = "MSBuild RDKit2DotNet.csproj /p:Configuration=Release,Platform=AnyCPU /maxcpucount"
            call_subprocess(cmd)
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

        replace_file_string(
            nuspec_file,
            [
                (
                    "\\<version\\>[0-9\\.]*\\<\\/version\\>",
                    f"<version>{self.get_version_for_nuget()}</version>",
                )
            ],
        )
        replace_file_string(
            nuspec_file,
            [
                (
                    "RDKit Release_\\d\\d\\d\\d\\_\\d\\d\\_\\d",
                    f"RDKit Release_{self.get_version_for_nuget().replace('.', '_')}",
                )
            ],
        )
        replace_file_string(
            nuspec_file,
            [("Boost \\d+\\.\\d+\\.\\d+", f"Boost {self.get_version_for_boost()}")],
        )
        replace_file_string(
            nuspec_file,
            [("Eigen \\d+\\.\\d+\\.\\d+", f"Eigen {self.get_version_for_eigen()}")],
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
            for p in ("RDKit.DotNetWrap.nuspec", "RDKit.DotNetWrap.targets",):
                    remove_if_exist(self.rdkit_path / "Code" / "JavaWrappers" / "csharp_wrapper" / p)
            remove_if_exist(self.rdkit_path / "lib")
            for p in cpu_models:
                remove_if_exist(self.rdkit_path / "Code" / "JavaWrappers" / "csharp_wrapper" / p)
                remove_if_exist(self.rdkit_path / f"build{p}CSharp")
        if self.config.freetype_path:
            for p in cpu_models:
                remove_if_exist(self.freetype_path / "objs" / _platform_to_ms_form[p])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--build_platform", choices=("x86", "x64", "all"),
    )
    parser.add_argument(
        "--disable_swig_patch", default=False, action="store_true",
    )
    parser.add_argument(
        "--build_freetype", default=False, action="store_true",
    )
    parser.add_argument(
        "--build_rdkit", default=False, action="store_true",
    )
    parser.add_argument(
        "--build_wrapper", default=False, action="store_true",
    )
    parser.add_argument(
        "--build_nuget", default=False, action="store_true",
    )
    parser.add_argument(
        "--rdkit_dir", type=str,
    )
    parser.add_argument(
        "--boost_dir", type=str,
    )
    parser.add_argument(
        "--eigen_dir", type=str,
    )
    parser.add_argument(
        "--freetype_dir", type=str,
    )
    parser.add_argument(
        "--clean", default=False, action="store_true",
    )
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
        swig_patch_enabled=not args.disable_swig_patch,
        this_path=here,
        rdkit_path=path_from_arg_or_env(args.rdkit_dir, "RDKITDIR"),
        boost_path=path_from_arg_or_env(args.boost_dir, "BOOSTDIR"),
        eigen_path=path_from_arg_or_env(args.eigen_dir, "EIGENDIR"),
        swig_path=path_from_arg_or_env(None, "SWIG_DIR"),
        freetype_path=path_from_arg_or_env(args.freetype_dir, "FREETYPEDIR"),
        number_of_processors=cast(int, get_value_from_env("NUMBER_OF_PROCESSORS", "1")),
        minor_version=cast(int, get_value_from_env("MINORVERSION", "1")),
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
