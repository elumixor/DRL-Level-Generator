using System;
using UnityEngine;

namespace Player {
    /// <summary>
    /// Handles input and sends corresponding commands to <see cref="PlayerBehaviouralController"/>
    /// </summary>
    [RequireComponent(typeof(PlayerBehaviouralController))]
    public class PlayerInputHandler : MonoBehaviour {
        void Update() {
            if (Input.GetMouseButtonDown(0)) {
                OnTap();
            }
        }

        public void OnTap() {
            var playerBehaviouralController = GetComponent<PlayerBehaviouralController>();
            
            playerBehaviouralController.Switch();
            playerBehaviouralController.Boost();
        }
    }
}