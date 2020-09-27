using System;
using System.Linq;
using DRL.Behaviours;
using NaughtyAttributes;
using Player;
using UnityEngine;

namespace Implementation {
    public class MyEnvironment : Environment<MyAction, MyObservation> {
        [SerializeField, Required] PlayerBehaviouralController player;
        [SerializeField, Required] PlayerInputHandler playerInputHandler;

        public override void ResetEnvironment() {
            player.ResetState();
            foreach (var followTransform in FindObjectsOfType<FollowTransform>()) followTransform.Synchronize();
        }

        public override (float reward, bool isDone) Step(MyAction action) {
            if (action.tap) {
                playerInputHandler.OnTap();
            }

            return (1f, false);
        }

        protected override MyObservation CurrentObservation {
            get {
                var enemies = FindObjectsOfType<Enemy>();
                var playerPosition = GameObject.FindWithTag("Player").transform.position;
                var minDistance = enemies.Select(e => (e.transform.position - playerPosition).magnitude).Min();
                
                return new MyObservation {distanceToClosest = minDistance};
            }
        }
    }
}