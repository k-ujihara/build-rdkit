using System;
using System.IO;
using System.Runtime.InteropServices;

namespace GraphMolWrap
{
    partial class RDKFuncsPINVOKE
    {
        private const string ModuleName = "RDKFuncs";

        [System.Security.SuppressUnmanagedCodeSecurity]
        internal static class UnsafeNativeMethods
        {
            [DllImport("kernel32", CharSet = CharSet.Unicode, SetLastError = true)]
            internal static extern bool SetDllDirectory(string lpPathName);
        }

        internal static void LoadDll()
        {
            var os = Environment.OSVersion;
            switch (os.Platform)
            {
                case PlatformID.Win32NT:
                    const string DllName = ModuleName + ".dll";
                    string currPath = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
                    string subdir = null;
                    if (Environment.Is64BitProcess)
                    {
                        subdir = "x64";
                    }
                    else
                    {
                        subdir = "x86";
                    }

                    if (subdir != null)
                    {
                        var path = Path.Combine(currPath, subdir);
                        var dllpath = Path.Combine(path, DllName);
                        if (File.Exists(dllpath))
                        {
                            UnsafeNativeMethods.SetDllDirectory(null);
                            UnsafeNativeMethods.SetDllDirectory(path);
                        }
                    }
                    break;
                default:
                    break;
            }
        }
    }
}
