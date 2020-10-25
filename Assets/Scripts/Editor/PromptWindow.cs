using System;
using UnityEditor;
using UnityEngine;

namespace Editor {
    public class PromptWindow : EditorWindow {
        bool isClosed;
        string label;
        Action reject;
        Action<string> resolve;
        string textValue = "";

        void OnGUI() {
            GUILayout.Label(label);
            GUI.SetNextControlName("textField");
            textValue = GUILayout.TextField(textValue);
            EditorGUI.FocusTextInControl("textField");

            if (GUILayout.Button("Ok")) {
                Resolve();
                return;
            }

            if (GUILayout.Button("Cancel")) {
                Reject();
            }
        }

        void OnLostFocus() { Reject(); }

        public static void Show(string label, Action<string> resolve, Action reject) {
            var window = GetWindow<PromptWindow>();
            window.label = label;
            window.resolve = resolve;
            window.reject = reject;
        }

        new void Close() {
            if (isClosed) return;
            isClosed = true;
            base.Close();
        }

        void Resolve() {
            Close();
            resolve(textValue);
        }

        void Reject() {
            Close();
            reject();
        }
    }
}