using System;
using Common;
using Configuration.AlgorithmConfigurations;
using UnityEditor;
using UnityEngine;
using static Configuration.AlgorithmNames;

namespace Configuration {
    public partial class Configuration {
        [CustomEditor(typeof(Configuration))]
        public class ConfigurationEditor : Editor {
            Configuration configuration;

            ConfigurationVPG.Editor editorVPG;
            ConfigurationA2C.Editor editorA2C;

            void OnEnable() {
                configuration = (Configuration) target;

                editorVPG = new ConfigurationVPG.Editor(configuration.configurationVPG);
                editorA2C = new ConfigurationA2C.Editor(configuration.configurationA2C);
            }

            public override void OnInspectorGUI() {
                serializedObject.Update();
                configuration.algorithm = (AlgorithmNames) EditorGUILayout.EnumPopup("Algorithm", configuration.algorithm);

                switch (configuration.algorithm) {
                    case VPG:
                        editorVPG.OnInspectorGUI();
                        break;
                    case A2C:
                        editorA2C.OnInspectorGUI();
                        break;
                    default:
                        throw new ArgumentOutOfRangeException();
                }
                
                serializedObject.ApplyModifiedProperties();
            }
        }
    }
}