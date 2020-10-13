using System;
using UnityEngine;

namespace Common {
    public class SingletonBehaviour<T> : MonoBehaviour where T : MonoBehaviour {
        static T instance;
        void Awake() => instance = GetComponent<T>();
    }
}