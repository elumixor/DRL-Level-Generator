using System;
using UnityEngine;

namespace Testing.PlayModeTests.Common
{
    public class Breaker : MonoBehaviour
    {
        public static event Action Break = delegate { };

        void Update()
        {
            if (Input.GetKeyDown(KeyCode.Escape)) Break();
        }
    }
}
