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
                    const string DllFileName = ModuleName + ".dll";
                    var subdir = Environment.Is64BitProcess ? "x64" : "x86";

                    var executingAsm = System.Reflection.Assembly.GetExecutingAssembly();
                    {
                        var currPath = Path.GetDirectoryName(executingAsm.Location);
                        if (SetDllDirectoryIfFileExist(currPath, subdir, DllFileName))
                            goto L_Found;
                    }
                    {
                        var uri = new Uri(executingAsm.CodeBase);
                        if (uri.Scheme == "file")
                        {
                            var currPath = Path.GetDirectoryName(uri.AbsolutePath);
                            if (SetDllDirectoryIfFileExist(currPath, subdir, DllFileName))
                                goto L_Found;
                        }
                    }
                L_Found:
                    break;
                default:
                    break;
            }
        }

        /// <summary>
        /// SetDllDirectory if <paramref name="directoryName"/>/<paramref name="subdir"/>/<paramref name="dllName"/> or <paramref name="directoryName"/>/<paramref name="dllName"/>exists.
        /// </summary>
        /// <param name="directoryName">Directory of the DLL.</param>
        /// <param name="subdir">Sub directory name, typically "x86" or "x64".</param>
        /// <param name="dllName">Base name of the DLL.</param>
        /// <returns><see langword="true"/> if file exists and set it.</returns>
        private static bool SetDllDirectoryIfFileExist(string directoryName, string subdir, string dllName)
        {
            if (subdir != null)
            {
                if (SetDllDirectoryIfFileExist(Path.Combine(directoryName, subdir), dllName))
                    return true;
            }

            if (SetDllDirectoryIfFileExist(directoryName, dllName))
                return true;

            return false;
        }

        /// <summary>
        /// SetDllDirectory if <paramref name="directoryName"/>/<paramref name="dllName"/> exists.
        /// </summary>
        /// <param name="directoryName">Directory of the DLL.</param>
        /// <param name="dllName">Base name of the DLL.</param>
        /// <returns><see langword="true"/> if file exists and set it.</returns>
        private static bool SetDllDirectoryIfFileExist(string directoryName, string dllName)
        {
            var dllPath = Path.Combine(directoryName, dllName);
            if (File.Exists(dllPath))
            {
                UnsafeNativeMethods.SetDllDirectory(null);
                UnsafeNativeMethods.SetDllDirectory(directoryName);
                return true;
            }
            return false;
        }        
    }
}
