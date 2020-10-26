using System;
using Configuration.AlgorithmConfigurations;
using UnityEditor;
using static Configuration.Algorithm;

namespace Configuration {
    public partial class TrainingSetupConfiguration {
        [CustomEditor(typeof(TrainingSetupConfiguration))]
        public class ConfigurationEditor : UnityEditor.Editor {
            ConfigurationA2C.Editor editorA2C;

            ConfigurationVPG.Editor editorVPG;
            TrainingSetupConfiguration trainingSetupConfiguration;

            void OnEnable() {
                trainingSetupConfiguration = (TrainingSetupConfiguration) target;

                editorVPG = new ConfigurationVPG.Editor(trainingSetupConfiguration.configurationVPG);
                editorA2C = new ConfigurationA2C.Editor(trainingSetupConfiguration.configurationA2C);
            }

            public override void OnInspectorGUI() {
                serializedObject.Update();
                trainingSetupConfiguration.algorithm =
                    (Algorithm) EditorGUILayout.EnumPopup("Algorithm", trainingSetupConfiguration.algorithm);

                switch (trainingSetupConfiguration.algorithm) {
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
                EditorUtility.SetDirty(target);
            }
        }
    }
}