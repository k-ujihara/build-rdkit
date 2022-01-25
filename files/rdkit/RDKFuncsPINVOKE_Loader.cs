using System;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;

namespace GraphMolWrap
{
    partial class RDKFuncsPINVOKE
    {
        private const string DllBaseName = "RDKFuncs";
        internal static bool loaded = false;

#if NETCOREAPP3_1
        /// <summary>
        /// Implementation of DllImportResolver.
        /// </summary>
        /// <param name="libraryName">library name to load</param>
        /// <param name="assembly">assembly loading</param>
        /// <param name="searchPath"></param>
        /// <returns></returns>
        /// <see href="https://docs.microsoft.com/ja-jp/dotnet/standard/native-interop/cross-platform"/>
        private static IntPtr DllImportResolver(string libraryName, Assembly assembly, DllImportSearchPath? searchPath)
        {
            if (libraryName == DllBaseName)
            {
                var os = Environment.OSVersion;
                string osname;
                string suffix;
                switch (os.Platform)
                {
                    case PlatformID.Win32NT:
                        osname = "win";
                        suffix = ".dll";
                        break;
                    case PlatformID.Unix:
                        osname = "linux";
                        suffix = ".so";
                        break;
                    default:
                        return IntPtr.Zero;

                }
                string cpu = Environment.Is64BitProcess ? "x64" : "x86";

                string filename = $"{DllBaseName}{suffix}";
                {
                    string pathToDll = Path.Combine(Path.GetDirectoryName(assembly.Location), "runtimes", $"{osname}-{cpu}", "native", filename);
                    if (File.Exists(pathToDll))
                        return NativeLibrary.Load(pathToDll, assembly, searchPath);
                }
                {
                    // ASP.NET
                    var uri = new Uri(assembly.CodeBase);
                    if (uri.Scheme == "file")
                    {
                        string pathToDll = Path.Combine(Path.GetDirectoryName(uri.AbsolutePath), "runtimes", $"{osname}-{cpu}", "native", filename);
                        if (File.Exists(pathToDll))
                            return NativeLibrary.Load(pathToDll, assembly, searchPath);
                    }
                }
            }
            return IntPtr.Zero;
        }

        internal static void LoadDll()
        {
            if (!loaded)
            {
                NativeLibrary.SetDllImportResolver(Assembly.GetExecutingAssembly(), DllImportResolver);
                loaded = true;
            }
        }
#else
        [System.Security.SuppressUnmanagedCodeSecurity]
        internal static class UnsafeNativeMethods
        {
            [DllImport("kernel32", CharSet = CharSet.Unicode, SetLastError = true)]
            internal static extern bool SetDllDirectory(string lpPathName);
        }

        internal static void LoadDll()
        {
            if (loaded)
                return;
            loaded = true;

            var os = Environment.OSVersion;
            switch (os.Platform)
            {
                case PlatformID.Win32NT:
                    const string DllFileName = DllBaseName + ".dll";
                    var cpu = Environment.Is64BitProcess ? "x64" : "x86";
                    var executingAsm = System.Reflection.Assembly.GetExecutingAssembly();
                    foreach (var subdir in new[] {
                        Path.Combine("runtimes", $"win-{cpu}", "native"),
                        cpu,
                    })
                    {
                        if (SetDllDirectoryIfFileExist(Path.GetDirectoryName(executingAsm.Location), subdir, DllFileName))
                            break;
                        // for ASP.NET
                        var uri = new Uri(executingAsm.CodeBase);
                        if (uri.Scheme == "file")
                        {
                            if (SetDllDirectoryIfFileExist(Path.GetDirectoryName(uri.AbsolutePath), subdir, DllFileName))
                                break;
                        }
                    }
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
            if (SetDllDirectoryIfFileExist(Path.Combine(directoryName, subdir), dllName))
                return true;

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
#endif
    }
}
