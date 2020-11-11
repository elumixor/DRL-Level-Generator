using System;
using UnityEngine;

namespace RL.Common
{
    public class SingletonBehaviour<T> : MonoBehaviour
            where T : MonoBehaviour
    {
        protected static T instance;

        protected virtual void Awake()
        {
            if (instance != null) throw new Exception($"There is more than one singleton behaviour of type [{typeof(T)}] in the scene.");

            instance = GetComponent<T>();
        }
    }
}
