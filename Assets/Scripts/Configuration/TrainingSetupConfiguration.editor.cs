﻿using System;
using Common;
using Configuration.AlgorithmConfigurations;
using UnityEditor;
using UnityEngine;
using static Configuration.Algorithm;

namespace Configuration {
    public partial class TrainingSetupConfiguration {
        [CustomEditor(typeof(TrainingSetupConfiguration))]
        public class ConfigurationEditor : Editor {
            TrainingSetupConfiguration trainingSetupConfiguration;

            ConfigurationVPG.Editor editorVPG;
            ConfigurationA2C.Editor editorA2C;

            void OnEnable() {
                trainingSetupConfiguration = (TrainingSetupConfiguration) target;

                editorVPG = new ConfigurationVPG.Editor(trainingSetupConfiguration.configurationVPG);
                editorA2C = new ConfigurationA2C.Editor(trainingSetupConfiguration.configurationA2C);
            }

            public override void OnInspectorGUI() {
                serializedObject.Update();
                trainingSetupConfiguration.algorithm = (Algorithm) EditorGUILayout.EnumPopup("Algorithm", trainingSetupConfiguration.algorithm);

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
            }
        }
    }
}