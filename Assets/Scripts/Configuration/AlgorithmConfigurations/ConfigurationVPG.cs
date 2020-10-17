using System;
using Common;
using Configuration.NN;

namespace Configuration.AlgorithmConfigurations {
    [Serializable]
    public class ConfigurationVPG : AlgorithmConfiguration {
        public Layout actor = new Layout();
        public override Layout ActorLayout => actor;

        public class Editor : IEditor {
            readonly Layout.Editor nnLayoutEditor;

            public Editor(ConfigurationVPG configurationVPG) { nnLayoutEditor = new Layout.Editor(configurationVPG.actor); }

            public void OnInspectorGUI() { nnLayoutEditor.OnInspectorGUI(); }
        }
    }
}