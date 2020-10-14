using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using NN;
using UnityEditor;
using UnityEngine;

namespace Configuration.NN {
    [Serializable]
    public class Layout {
        public List<ModuleConfiguration> modules = new List<ModuleConfiguration>();
        bool displayed;

        public class Editor : IEditor {
            enum LayerAction {
                None,
                Remove,
                Copy,
                MoveUp,
                MoveDown,
            }

            readonly Layout layout;
            readonly string label;

            public Editor(Layout layout, string label = null) {
                this.layout = layout;
                this.label = label;
            }

            public void OnInspectorGUI() {
                layout.displayed = EditorGUILayout.Foldout(layout.displayed, label ?? "NN Layout", true);

                if (!layout.displayed) return;

                var layerAction = LayerAction.None;
                var actingIndex = -1;

                for (var i = 0; i < layout.modules.Count; i++) {
                    var layer = layout.modules[i];
                    var action = OnLayerGUI(layer);
                    if (layerAction == LayerAction.None && action != LayerAction.None) {
                        layerAction = action;
                        actingIndex = i;
                    }
                }

                if (layerAction != LayerAction.None) PerformAction(layerAction, actingIndex);

                if (GUILayout.Button("Add layer")) layout.modules.Add(new ModuleConfiguration());
            }

            static LayerAction OnLayerGUI(ModuleConfiguration module) {
                var (layerName, floatParameters, intParameters) = module;

                var action = LayerAction.None;

                using (new GUILayout.HorizontalScope()) {
                    module.layerName = (ModuleLayerName) EditorGUILayout.EnumPopup(layerName);

                    if (GUILayout.Button("↑")) action = LayerAction.MoveUp;
                    if (GUILayout.Button("↓")) action = LayerAction.MoveDown;
                    if (GUILayout.Button("+")) action = LayerAction.Copy;
                    if (GUILayout.Button("-")) action = LayerAction.Remove;
                }

                using (new GUILayout.HorizontalScope()) {
                    using (new GUILayout.VerticalScope()) {
                        GUILayout.Label("Int Parameters");
                        OnParametersGUI(intParameters, v => EditorGUILayout.IntField(v));
                    }

                    using (new GUILayout.VerticalScope()) {
                        GUILayout.Label("Float Parameters");
                        OnParametersGUI(floatParameters, v => EditorGUILayout.FloatField(v));
                    }
                }

                return action;
            }

            static void OnParametersGUI<TKey, TValue>(IDictionary<TKey, TValue> parameters, Func<TValue, TValue> editorField)
                where TKey : Enum where TValue : struct {
                // TU replacementValue = default;
                // T changeKeyNew = default;
                // T currentKey = default;

                var changeKey = false;
                var changeValue = false;

                TKey oldKey = default;
                TKey newKey = default;
                TValue newValue = default;

                foreach (var parameter in parameters.Where(parameter => !Equals(parameter.Key, default(TKey)))) {
                    using (new GUILayout.HorizontalScope()) {
                        var newK = (TKey) EditorGUILayout.EnumPopup(parameter.Key);

                        if (!Equals(newK, parameter.Key)) {
                            changeKey = true;
                            newKey = newK;
                            oldKey = parameter.Key;
                        }

                        var newV = editorField(parameter.Value);
                        if (!Equals(newV, parameters[parameter.Key])) {
                            changeValue = true;
                            newValue = newV;
                            newKey = parameter.Key;
                        }
                    }
                }

                if (changeValue) parameters[newKey] = newValue;

                if (changeKey) {
                    if (Equals(newKey, default(TKey))) {
                        parameters.Remove(oldKey);
                    } else {
                        var temp = parameters[newKey];
                        parameters[newKey] = parameters[oldKey];
                        parameters[oldKey] = temp;
                    }
                }

                var remaining = ((TKey[]) Enum.GetValues(typeof(TKey))).Where(p => !Equals(p, default) && !parameters.ContainsKey(p))
                    .ToArray();

                TKey toAdd = default;
                foreach (var parameterInt in remaining)
                    if (GUILayout.Button($"Add parameter: {parameterInt.ToString()}"))
                        toAdd = parameterInt;

                if (!Equals(toAdd, default)) parameters[toAdd] = default;
            }

            void PerformAction(LayerAction layerAction, int actingIndex) {
                switch (layerAction) {
                    case LayerAction.None:
                        return;
                    case LayerAction.Remove:
                        layout.modules.RemoveAt(actingIndex);
                        return;
                    case LayerAction.Copy:
                        layout.modules.Insert(actingIndex, layout.modules[actingIndex].Copy());
                        return;
                    case LayerAction.MoveUp: {
                        if (actingIndex == 0) return;

                        var temp = layout.modules[actingIndex - 1];
                        layout.modules[actingIndex - 1] = layout.modules[actingIndex];
                        layout.modules[actingIndex] = temp;
                        return;
                    }
                    case LayerAction.MoveDown: {
                        if (actingIndex == layout.modules.Count - 1) return;

                        var temp = layout.modules[actingIndex + 1];
                        layout.modules[actingIndex + 1] = layout.modules[actingIndex];
                        layout.modules[actingIndex] = temp;
                        return;
                    }
                    default:
                        return;
                }
            }
        }
    }
}