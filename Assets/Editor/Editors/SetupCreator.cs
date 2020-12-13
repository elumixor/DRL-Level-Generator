using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEngine;

namespace Editor.Editors
{
    public static class SetupCreator
    {
        const string TRAINING_SETUPS_PATH = "TrainingSetups";
        const string BOILERPLATE_PATH = "_Boilerplate";
        const string BOILERPLATE_NAME = "Boilerplate";

        [MenuItem("DRL/Create Training Setup")] static void CreateSetup() { PromptWindow.Show("Label", CreateSetup, () => { }); }

        static void CreateSetup(string name)
        {
            var basePath = $"{Application.dataPath}/{TRAINING_SETUPS_PATH}";

            CopyDirectoryRecursivelyWithNewName($"{basePath}/{BOILERPLATE_PATH}", $"{basePath}/{name}");
            basePath = $"{basePath}/{name}";

            // Rename scene
            var scenePath = $"{basePath}/{name}.unity";
            File.Move($"{basePath}/{BOILERPLATE_NAME}.unity", scenePath);

            // Rename asmdef
            File.Move($"{basePath}/{BOILERPLATE_NAME}.asmdef", $"{basePath}/{name}.asmdef");

            // Replace amsdef name
            File.WriteAllText($"{basePath}/{name}.asmdef",
                              Regex.Replace(File.ReadAllText($"{basePath}/{name}.asmdef"), "\"name\": \"(.*)\"", $"\"name\": \"{name}\""));

            AssetDatabase.Refresh();
        }

        static string GetAsmdefContents(string name) =>
                $@"{{
                ""name"": ""{name}"",
                ""references"": [
                ""GUID:aa0490c95e36e484d91e2347678fd417"",
                ""GUID:776d03a35f1b52c4a9aed9f56d7b4229""
                    ],
                ""includePlatforms"": [],
                ""excludePlatforms"": [],
                ""allowUnsafeCode"": false,
                ""overrideReferences"": false,
                ""precompiledReferences"": [],
                ""autoReferenced"": true,
                ""defineConstraints"": [],
                ""versionDefines"": [],
                ""noEngineReferences"": false
            }}";

        static void CopyDirectoryRecursivelyWithNewName(string sourcePath, string destinationPath)
        {
            //Now Create all of the directories
            foreach (var dirPath in Directory.GetDirectories(sourcePath, "*", SearchOption.AllDirectories))
                Directory.CreateDirectory(dirPath.Replace(sourcePath, destinationPath));

            //Copy all the files & Replaces any files with the same name
            foreach (var newPath in Directory.GetFiles(sourcePath, "*.*", SearchOption.AllDirectories).Where(f => !f.EndsWith(".meta")))
                File.Copy(newPath, newPath.Replace(sourcePath, destinationPath), true);
        }
    }
}
