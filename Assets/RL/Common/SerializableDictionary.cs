using System;
using System.Collections.Generic;
using UnityEngine;

namespace RL.Common
{
    [Serializable]
    public class SerializableDictionary<TKey, TValue> : Dictionary<TKey, TValue>, ISerializationCallbackReceiver
    {
        [SerializeField] List<TKey> keys = new List<TKey>();
        [SerializeField] List<TValue> values = new List<TValue>();

        public SerializableDictionary() { }
        public SerializableDictionary(int capacity) : base(capacity) { }

        public void OnBeforeSerialize()
        {
            keys.Clear();
            values.Clear();

            foreach (var kvp in this) {
                keys.Add(kvp.Key);
                values.Add(kvp.Value);
            }
        }

        public void OnAfterDeserialize()
        {
            Clear();

            var length = Math.Min(keys.Count, values.Count);
            for (var i = 0; i < length; i++) Add(keys[i], values[i]);
        }
    }
}
