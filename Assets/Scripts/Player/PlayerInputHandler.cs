using System;
using UnityEngine;

namespace Player {
    /// <summary>
    /// Handles input and sends corresponding commands to <see cref="PlayerBehaviouralController"/>
    /// </summary>
    [RequireComponent(typeof(PlayerBehaviouralController))]
    public class PlayerInputHandler : MonoBehaviour {
        private void Update() {
            if (Input.GetMouseButtonDown(0)) {
                Switch();
            }
        }

        private void Switch() {
            var playerBehaviouralController = GetComponent<PlayerBehaviouralController>();
            
            playerBehaviouralController.Switch();
            playerBehaviouralController.Boost();
        }
    }
}