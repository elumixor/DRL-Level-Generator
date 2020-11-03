using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using Configuration.Dynamic;
using JetBrains.Annotations;
using UnityEditor;
using UnityEditorInternal;
using UnityEngine;

namespace Editor.Editors
{
    [CustomEditor(typeof(LayoutSO))]
    public class LayoutSOEditor : RichEditor
    {
        LayoutSO layoutSO;
        List<Definition> Definitions => layoutSO.definitions;

        static GUIStyle basicModuleStyle;
        static GUIStyle customModuleStyle;
        static GUIStyle centeredLabelStyle;

        bool initialized;
        ReorderableList definitionsList;

        List<ReorderableList> submodulesListInDefinitions;

        bool Init()
        {
            if (initialized && definitionsList != null) return true;

            layoutSO = (LayoutSO) target;

            try {
                basicModuleStyle   = new GUIStyle(EditorStyles.boldLabel) {normal = {textColor = new Color(0.07f, 0.16f, 0.36f)}};
                customModuleStyle  = new GUIStyle(EditorStyles.boldLabel) {normal = {textColor = new Color(0.36f, 0.16f, 0.09f)}};
                centeredLabelStyle = new GUIStyle(EditorStyles.label) {alignment  = TextAnchor.MiddleCenter};

                UpdateModulesLists();

                definitionsList = new ReorderableList(serializedObject, serializedObject.FindProperty("definitions")) {
                        displayAdd            = false,
                        drawElementCallback   = DefinitionGUI,
                        elementHeightCallback = DefinitionHeight,
                        drawHeaderCallback    = DefinitionHeaderGUI,
                        onRemoveCallback =
                                _ => UpdateModulesLists(),
                };

                return initialized = true;
            } catch (Exception e) {
                Debug.LogException(e);
                return initialized = false;
            }
        }

        void UpdateModulesLists()
        {
            ReorderableList CreateSubmodulesList(Definition _, int definitionIndex)
            {
                var submodulesProperty = serializedObject.FindProperty("definitions")
                                                         .GetArrayElementAtIndex(definitionIndex)
                                                         .FindPropertyRelative("submodules");

                return new ReorderableList(serializedObject, submodulesProperty, true, false, false, true) {
                        headerHeight          = 0,
                        elementHeightCallback = moduleIndex => ModuleHeight(definitionIndex, moduleIndex),
                        drawElementCallback = (position, moduleIndex, isactive, isfocused) =>
                                ModuleGUI(position, definitionIndex, moduleIndex, isactive, isfocused),
                        onReorderCallback = delegate { UpdateModulesLists(); },
                };
            }

            submodulesListInDefinitions = new List<ReorderableList>(Definitions.Select(CreateSubmodulesList));
        }

        static void DefinitionHeaderGUI(Rect rect) => EditorGUI.LabelField(rect, "Definitions");

        string currentDefitionName = "";

        /// <inheritdoc/>
        public override void OnInspectorGUI()
        {
            if (!Init()) return;

            serializedObject.Update();

            using (new EditorGUILayout.HorizontalScope()) {
                currentDefitionName = EditorGUILayout.TextField("Add module definition", currentDefitionName);

                if (GUILayout.Button("Add") && currentDefitionName != "") {
                    Definitions.Add(new Definition(currentDefitionName));
                    currentDefitionName = "";
                }
            }

            definitionsList.DoLayoutList();
            serializedObject.ApplyModifiedProperties();

            EditorUtility.SetDirty(layoutSO);
        }

        #region Definition
        void DefinitionGUI(Rect position, int definitionIndex, bool isactive, bool isfocused)
        {
            // Draw background box
            position.y      += Spacing;
            position.height -= Spacing * 2;
            GUI.Box(position, GUIContent.none);

            position.y += Spacing;
            position.x += 2 * Spacing;

            position.width  -= Spacing * 4;
            position.height -= Spacing * 2;

            var definition = Definitions[definitionIndex];

            // Display and edit the name of the definition
            definition.name = EditorGUI.TextField(new Rect(position) {height = LineHeight}, definition.name, customModuleStyle);

            // Popup to add new module
            position.y += LineHeight + Spacing;
            var selected = SelectModuleGUIPopup(new Rect(position) {height = LineHeight}, definitionIndex, null, "Add module");

            if (selected != null) {
                definition.submodules.Add(new Module(selected));
                UpdateModulesLists();
            }

            // Draw submodules
            if (definition.submodules.IsEmpty()) return;

            position.y += LineHeight + Spacing;
            var modulesRect = new Rect(position) {height = GetModulesHeight(definitionIndex)};
            submodulesListInDefinitions[definitionIndex].DoList(modulesRect);
        }

        float DefinitionHeight(int definitionIndex)
        {
            var boxOuterSpacing = Spacing * 2;
            var boxInnerSpacing = Spacing * 2;
            var numLines = 2;
            return LineHeight * numLines + Spacing * (numLines - 1) + boxOuterSpacing + boxInnerSpacing + GetModulesHeight(definitionIndex);
        }
        #endregion

        #region Mogule
        void ModuleGUI(Rect position, int definitionIndex, int moduleIndex, bool isActive, bool isFocused)
        {
            position.y      += Spacing;
            position.height -= Spacing * 2;

            var module = Definitions[definitionIndex].submodules[moduleIndex];
            var definitionName = module.definitionName;
            var w = position.width - 2 * Spacing;

            // 30 35 35 split. all in one line
            var nameRect = new Rect(position) {width = .3f * w};
            var inputsRect = new Rect(position) {
                    width = .35f * w,
                    x     = .3f * w + Spacing + position.x,
            };
            var outputsRect = new Rect(position) {
                    width = .35f * w,
                    x     = .65f * w + Spacing + Spacing + position.x,
            };

            // Standard Definitions
            var newModule = SelectModuleGUIPopup(nameRect, definitionIndex, definitionName);
            if (newModule != null) module.definitionName = newModule;

            // Input
            var (mustInferInput, mustSpecifyInput) = GetModuleInputInferenceFlags(definitionIndex, moduleIndex);

            if (!mustInferInput && !mustSpecifyInput) {
                var inputsWidth = module.inputSizeInferred ? inputsRect.width : (inputsRect.width - Spacing) / 2;
                var inputsText = module.inputSizeInferred ? "Input size: Inferred" : "Input size:";
                if (GUI.Button(new Rect(inputsRect) {width = inputsWidth}, inputsText)) module.inputSizeInferred = !module.inputSizeInferred;

                if (!module.inputSizeInferred)
                    module.inputSizeFixed = EditorGUI.IntField(new Rect(inputsRect) {
                                                                       width = inputsWidth,
                                                                       x =
                                                                               inputsRect.x + inputsWidth + Spacing,
                                                               },
                                                               module.inputSizeFixed);
            } else if (mustInferInput)
                GUI.Label(new Rect(inputsRect), "Input size inferred", centeredLabelStyle);
            else {
                var inputsWidth = (inputsRect.width - Spacing) / 2;
                EditorGUI.LabelField(new Rect(inputsRect) {width = inputsWidth},
                                     "Input size:",
                                     new GUIStyle(EditorStyles.label) {alignment = TextAnchor.MiddleCenter});

                var numberInputRect = new Rect(inputsRect) {
                        width = inputsWidth,
                        x     = inputsRect.x + inputsWidth + Spacing,
                };

                module.inputSizeFixed = EditorGUI.IntField(numberInputRect, module.inputSizeFixed);
            }

            // Output
            var (mustInferOutput, mustSpecifyOutput) = GetModuleOutputInferenceFlags(definitionIndex, moduleIndex);

            if (!mustInferOutput && !mustSpecifyOutput) {
                var outputsWidth = module.outputSizeInferred ? outputsRect.width : (outputsRect.width - Spacing) / 2;
                var outputsText = module.outputSizeInferred ? "Output size: Inferred" : "Output size:";
                if (GUI.Button(new Rect(outputsRect) {width = outputsWidth}, outputsText)) module.outputSizeInferred = !module.outputSizeInferred;

                if (!module.outputSizeInferred)
                    module.outputSizeFixed = EditorGUI.IntField(new Rect(outputsRect) {
                                                                        width = outputsWidth,
                                                                        x     = outputsRect.x + outputsWidth + Spacing,
                                                                },
                                                                module.outputSizeFixed);
            } else if (mustInferOutput)
                GUI.Label(new Rect(outputsRect), "Output size inferred", centeredLabelStyle);
            else {
                var outputsWidth = (outputsRect.width - Spacing) / 2;
                EditorGUI.LabelField(new Rect(outputsRect) {width = outputsWidth},
                                     "Output size:",
                                     new GUIStyle(EditorStyles.label) {alignment = TextAnchor.MiddleCenter});
                module.outputSizeFixed = EditorGUI.IntField(new Rect(outputsRect) {
                                                                    width = outputsWidth,
                                                                    x =
                                                                            outputsRect.x + outputsWidth + Spacing,
                                                            },
                                                            module.outputSizeFixed);
            }
        }

        float ModuleHeight(int definitionIndex, int moduleIndex) => LineHeight + Spacing * 2;
        #endregion

        float GetModulesHeight(int definitionIndex)
        {
            var definition = Definitions[definitionIndex];
            var submodulesCount = definition.SubmodulesCount;
            if (submodulesCount == 0) return 0;

            return Enumerable.Range(0, submodulesCount).Select(moduleIndex => ModuleHeight(definitionIndex, moduleIndex)).Sum()
                 + submodulesListInDefinitions[definitionIndex].footerHeight + 5;
        }

        [CanBeNull]
        string SelectModuleGUIPopup(Rect position, int definitionIndex, string selected = null, string actionOptionName = null)
        {
            var predefinedModulesNames = Definition.Predefined.Select(module => module.name).ToArray();
            var customModulesNames = Definitions.Select(definition => definition.name).Take(definitionIndex).ToArray();

            var hasActionLabel = !string.IsNullOrEmpty(actionOptionName);

            int selectedIndex;

            if (selected == null)
                selectedIndex = 0;
            else {
                var predefinedIndex = Array.IndexOf(predefinedModulesNames, selected);
                selectedIndex = (predefinedIndex < 0 ? Array.IndexOf(customModulesNames, selected) + Definition.Predefined.Length : predefinedIndex)
                              + (hasActionLabel ? 1 : 0);
            }

            if (hasActionLabel) {
                var options = actionOptionName.Yield().Concat(predefinedModulesNames).Concat(customModulesNames).ToArray();
                var newIndex = EditorGUI.Popup(position, selectedIndex, options);

                if (selectedIndex == newIndex || newIndex == 0) return null;

                newIndex -= 1;
                if (newIndex < Definition.Predefined.Length) return Definition.Predefined[newIndex].name; // Return a copy of a predefined to avoid modification

                newIndex -= Definition.Predefined.Length;
                return Definitions[newIndex].name;
            } else {
                var options = predefinedModulesNames.Concat(customModulesNames).ToArray();

                var newIndex = EditorGUI.Popup(position, selectedIndex, options);

                if (selectedIndex == newIndex) return null;

                if (newIndex < Definition.Predefined.Length) return Definition.Predefined[newIndex].name; // Return a copy of a predefined to avoid modification

                newIndex -= Definition.Predefined.Length;
                return Definitions[newIndex].name;
            }
        }

        (bool mustInfer, bool mustSpecify) GetModuleInputInferenceFlags(int definitionIndex, int moduleIndex)
        {
            var module = Definitions[definitionIndex][moduleIndex];
            var notFirstSubmodule = moduleIndex > 0;

            if (module.definitionName == Definition.ReLU.name || module.definitionName == Definition.Softmax.name) return (notFirstSubmodule, false);

            if (module.definitionName == Definition.Linear.name) {
                var mustInfer = notFirstSubmodule   && ProvidesOutput(definitionIndex, moduleIndex - 1);
                var mustSpecify = notFirstSubmodule && !ProvidesOutput(definitionIndex, moduleIndex - 1);
                return (mustInfer, mustSpecify);
            }

            // Defined module
            {
                var hasFixedInput = HasFixedInput(module.definitionName);
                var mustInfer = hasFixedInput || notFirstSubmodule && ProvidesOutput(definitionIndex, moduleIndex     - 1);
                var mustSpecify = !hasFixedInput && notFirstSubmodule && !ProvidesOutput(definitionIndex, moduleIndex - 1);

                return (mustInfer, mustSpecify);
            }
        }

        (bool mustInfer, bool mustSpecify) GetModuleOutputInferenceFlags(int definitionIndex, int moduleIndex)
        {
            var module = Definitions[definitionIndex][moduleIndex];
            var notLastSubmodule = moduleIndex < Definitions[definitionIndex].SubmodulesCount - 1;

            if (module.definitionName == Definition.ReLU.name || module.definitionName == Definition.Softmax.name) return (notLastSubmodule, false);

            if (module.definitionName == Definition.Linear.name) {
                var mustSpecify = notLastSubmodule && !ProvidesInput(definitionIndex, moduleIndex + 1);
                return (false, mustSpecify);
            }

            // Defined module
            {
                var hasFixedOutput = HasFixedOutput(module.definitionName);
                var mustInfer = hasFixedOutput || notLastSubmodule && ProvidesInput(definitionIndex, moduleIndex     + 1);
                var mustSpecify = !hasFixedOutput && notLastSubmodule && !ProvidesInput(definitionIndex, moduleIndex + 1);
                return (mustInfer, mustSpecify);
            }
        }

        bool ProvidesOutput(int definitionIndex, int moduleIndex)
        {
            var module = Definitions[definitionIndex][moduleIndex];
            var isFirst = moduleIndex == 0;

            if (module.definitionName == Definition.ReLU.name || module.definitionName == Definition.Softmax.name)
                return isFirst || ProvidesOutput(definitionIndex, moduleIndex - 1);
            if (module.definitionName == Definition.Linear.name) return !module.outputSizeInferred;

            // Defined module
            if (HasFixedOutput(module.definitionName)) return true;

            return isFirst || ProvidesOutput(definitionIndex, moduleIndex - 1);
        }

        bool ProvidesInput(int definitionIndex, int moduleIndex)
        {
            var module = Definitions[definitionIndex].submodules[moduleIndex];
            var isLast = moduleIndex == Definitions[definitionIndex].SubmodulesCount - 1;

            if (module.definitionName == Definition.ReLU.name || module.definitionName == Definition.Softmax.name)
                return isLast || ProvidesInput(definitionIndex, moduleIndex + 1);

            if (module.definitionName == Definition.Linear.name) return !module.inputSizeInferred;

            // Defined module
            if (HasFixedInput(module.definitionName)) return true;

            return isLast || ProvidesInput(definitionIndex, moduleIndex + 1);
        }

        bool HasFixedInput(string definitionName)
        {
            var definition = Definitions.Find(d => d.name == definitionName);
            return !definition[0].inputSizeInferred;
        }

        bool HasFixedOutput(string definitionName)
        {
            var definition = Definitions.Find(d => d.name == definitionName);
            return !definition[definition.SubmodulesCount - 1].outputSizeInferred;
        }
    }
}
