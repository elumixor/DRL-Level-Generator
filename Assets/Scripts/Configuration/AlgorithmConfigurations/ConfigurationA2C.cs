using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;
using Configuration.NN;
using UnityEditor;

namespace Configuration.AlgorithmConfigurations {
    [Serializable]
    public class ConfigurationA2C : AlgorithmConfiguration {
        public enum A2CNetworksType {
            TwoHeaded,
            Separate,
        }

        public Layout actor = new Layout();

        public Layout actorHead = new Layout();

        public Layout @base = new Layout();

        public Layout critic = new Layout();

        public Layout criticHead = new Layout();

        public A2CNetworksType networksType;

        public override Layout ActorLayout => actor;

        public override IEnumerable<byte> ToBytes() {
            var networksBytes = networksType == A2CNetworksType.Separate
                                    ? actor.ToBytes().Concat(critic.ToBytes())
                                    : @base.ToBytes().ConcatMany(actorHead.ToBytes(), criticHead.ToBytes());

            return networksType.ToString().ToBytes().Concat(networksBytes);
        }

        public class Editor : IEditor {
            readonly Layout.Editor actorEditor;
            readonly Layout.Editor actorHeadEditor;

            readonly Layout.Editor baseEditor;
            readonly ConfigurationA2C configuration;
            readonly Layout.Editor criticEditor;
            readonly Layout.Editor criticHeadEditor;

            public Editor(ConfigurationA2C configuration) {
                this.configuration = configuration;
                actorEditor = new Layout.Editor(configuration.actor, "Actor");
                criticEditor = new Layout.Editor(configuration.critic, "Critic");

                baseEditor = new Layout.Editor(configuration.@base, "Base");
                criticHeadEditor = new Layout.Editor(configuration.actorHead, "Actor Head");
                actorHeadEditor = new Layout.Editor(configuration.criticHead, "Critic Head");
            }

            public void OnInspectorGUI() {
                configuration.networksType = (A2CNetworksType) EditorGUILayout.EnumPopup("NN Architecture", configuration.networksType);

                if (configuration.networksType == A2CNetworksType.Separate) {
                    actorEditor.OnInspectorGUI();
                    criticEditor.OnInspectorGUI();
                } else {
                    baseEditor.OnInspectorGUI();
                    criticHeadEditor.OnInspectorGUI();
                    actorHeadEditor.OnInspectorGUI();
                }
            }
        }
    }
}