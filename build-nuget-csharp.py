import glob
import os
import re
import shutil
import subprocess

cpu_models = [ 'x86', 'x64' ]
project_name = 'RDKit.DotNetWrap'

curr_dir = os.getcwd()

def replace_file_string(filename, pattern_replace):
    with open(filename, 'r', encoding="utf-8") as file:
        filedata = file.read()
        for pattern, replace in pattern_replace:
            filedata = re.sub(pattern, replace, filedata, flags=re.MULTILINE | re.DOTALL)
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(filedata)

this_dir: str = os.environ['THISDIR']
boost_dir = os.environ['BOOSTDIR']
rdkit_dir = os.environ['RDKITDIR']
s = re.split('[\\\\\\/]rdkit\\-Release_(\\d\\d\\d\\d)_(\\d\\d)_(\\d)', rdkit_dir)
if len(s) == 5 and (s[4] == '' or s[4] == '/' or s[4] == '\\'):
    version_for_nuget = f"0.{s[1]}{s[2]}{s[3]}.1"
    version_for_rdkit = f"{s[1]}.{s[2]}.{s[3]}"
else:
    version_for_nuget = ''
    version_for_rdkit = ''
rdkit_csharp_wrapper_dir = os.path.join(rdkit_dir, 'Code/JavaWrappers/csharp_wrapper')
rdkit_csharp_release_dir = os.path.join(rdkit_csharp_wrapper_dir, 'bin/Release')

skip_text_list = [ 'python', 'numpy' ]
dllfiles_dic = {}

def copy_and_add_dll(file: str, dllnames):
    dllname = os.path.basename(file)
    for skip_text in skip_text_list:
        if skip_text in dllname:
            break
    else:
        dllnames.append(dllname)
        shutil.copy2(file, dest_dir)

for cpu_model in cpu_models:
    dest_dir = os.path.join(rdkit_csharp_wrapper_dir, cpu_model)
    os.makedirs(dest_dir, exist_ok = True)
    dllnames = []
    copy_and_add_dll(rdkit_csharp_release_dir + '/'  + cpu_model + '/RDKFuncs.dll', dllnames)
    for file in glob.glob(os.path.join(boost_dir, 'stage/' + cpu_model + '/lib/*.dll')):
        copy_and_add_dll(file, dllnames)
    dllfiles_dic[cpu_model] = dllnames

# Prepare RDKit2DotNet.nuspec

nuspec_file = shutil.copy(os.path.join(this_dir, 'csharp_wrapper/' + project_name + '.nuspec'), rdkit_csharp_wrapper_dir)

if not version_for_nuget == '':
    replace_file_string(nuspec_file, [('\\<version\\>[0-9\\.]*\\<\\/version\\>', '<version>' + version_for_nuget + '</version>')])
    replace_file_string(nuspec_file, [('Release_\\d\\d\\d\\d\\.\\d\\d\\.\\d', 'Release_' + version_for_rdkit + '')])

nuspec_dlls_spec = []
for cpu_model in cpu_models:
    for dllname in dllfiles_dic[cpu_model]:
        nuspec_dlls_spec.append('<file src="' + cpu_model + '/' + dllname + '" target="runtimes/win-' + cpu_model + '/native" />\\n')

replace_file_string(nuspec_file, [('\\<nativefiles\\s*\\/\\>', ''.join(nuspec_dlls_spec))])

targets_file = shutil.copy(os.path.join(this_dir, 'csharp_wrapper/' + project_name + '.targets'), rdkit_csharp_wrapper_dir)
targets_dlls_spec = []
for cpu_model in cpu_models:
    targets_dlls_spec.append('<ItemGroup Condition=" \'$(Platform)\' == \'' + cpu_model +'\' ">\\n')
    for dllname in dllfiles_dic[cpu_model]:
        targets_dlls_spec.append('<None Include="$(MSBuildThisFileDirectory)../runtimes/win-' + cpu_model + '/native/' + dllname + '">\\n')
        targets_dlls_spec.append('<Link>' + dllname + '</Link>\\n')
        targets_dlls_spec.append('<CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>\\n')
        targets_dlls_spec.append('</None>\\n')
    targets_dlls_spec.append('</ItemGroup>\\n')

targets_dlls_spec.append('<ItemGroup Condition=" \'$(Platform)\' == \'' + 'AnyCPU' +'\' ">\\n')

for cpu_model in cpu_models:
    for dllname in dllfiles_dic[cpu_model]:
        targets_dlls_spec.append('<None Include="$(MSBuildThisFileDirectory)../runtimes/win-' + cpu_model + '/native/' + dllname + '">\\n')
        targets_dlls_spec.append('<Link>' + cpu_model + '/' + dllname + '</Link>\\n')
        targets_dlls_spec.append('<CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>\\n')
        targets_dlls_spec.append('</None>\\n')

targets_dlls_spec.append('</ItemGroup>')
replace_file_string(targets_file, [('\\<nativefiles\\s*\\/\\>', ''.join(targets_dlls_spec))])

os.chdir(rdkit_csharp_wrapper_dir)
cmd = 'nuget pack "' + project_name + '.nuspec" -Prop Configuration=Release -IncludeReferencedProjects'
subprocess.check_call(cmd)

os.chdir(curr_dir)
