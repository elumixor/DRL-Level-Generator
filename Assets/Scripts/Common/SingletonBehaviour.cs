using System;
using UnityEngine;

namespace Common {
    public class SingletonBehaviour<T> : MonoBehaviour where T : MonoBehaviour {
        static T instance;

        void Awake() {
            if (instance != null) throw new Exception($"There is more than one singleton behaviour of type [{typeof(T)}] in the scene.");

            instance = GetComponent<T>();
        }
    }
}