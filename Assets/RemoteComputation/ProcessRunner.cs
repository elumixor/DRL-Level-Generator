using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using JetBrains.Annotations;
using Debug = UnityEngine.Debug;

namespace RemoteComputation
{
    public static class ProcessRunner
    {
        public const string BACKEND_BASE_DIRECTORY = "C:/dev/DRL-Level-Generator/python/";
        public const string BASE_SOURCES_DIR = BACKEND_BASE_DIRECTORY + "src/";
        public const string BASE_TESTS_DIR = BACKEND_BASE_DIRECTORY   + "tests/";
        public const string PYTHON_COMMAND = "C:/Program Files/Python37/python.exe";

        public const string WORKING_DIR_PARAMETER_NAME = "working_directory";

        public static Process CreateProcess(string path,
                                            IDictionary<string, string> arguments = null,
                                            bool redirectStandardInput = true,
                                            bool redirectStandardOutput = true,
                                            bool useTestDir = false,
                                            bool separateWindow = false)
        {
            var dir = useTestDir ? BASE_TESTS_DIR : BASE_SOURCES_DIR;
            var argumentsString = $"\"{BACKEND_BASE_DIRECTORY}{path}\" {ParseArguments(arguments, dir)}";

#if UNITY_EDITOR
            Debug.Log($"Running command: {PYTHON_COMMAND} {argumentsString}");
#else
        Console.WriteLine($"Running command: {PYTHON_COMMAND} {argumentsString}");
#endif

            return new Process {
                    StartInfo = new ProcessStartInfo {
                            FileName               = PYTHON_COMMAND,
                            Arguments              = argumentsString,
                            CreateNoWindow         = !separateWindow,
                            RedirectStandardInput  = !separateWindow && redirectStandardInput,
                            RedirectStandardOutput = !separateWindow && redirectStandardOutput,
                            UseShellExecute        = separateWindow,
                    },
            };
        }

        static string ParseArguments([CanBeNull] IDictionary<string, string> arguments, string dir)
        {
            return $"--{WORKING_DIR_PARAMETER_NAME} \"{dir}\" "
                 + (arguments == null ? "" : string.Join(" ", arguments.Select(kvp => $"--{kvp.Key} \"{kvp.Value}\"")));
        }
    }
}
