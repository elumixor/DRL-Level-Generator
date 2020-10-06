using System;
using System.Linq;
using DRL.Behaviours;
using Implementation.Dummy;
using NaughtyAttributes;
using Player;
using UnityEngine;

namespace Implementation.PythonInference {
    public class InferenceEnvironment : Environment<DummyAction, State> {
        [SerializeField, Required] PlayerBehaviouralController player;
        [SerializeField, Required] PlayerInputHandler playerInputHandler;

        bool isDone;

        void Start() => player.Collided += () => {
            Debug.Log("Collided!");
            isDone = true;
        };

        public override void ResetEnvironment() {
            player.ResetState();
            isDone = false;
            foreach (var followTransform in FindObjectsOfType<FollowTransform>()) followTransform.Synchronize();
        }

        public override (float reward, bool isDone) Step(DummyAction action) {
            if (action.tap) playerInputHandler.OnTap();

            return (player.Position.y, isDone);
        }

        protected override State CurrentState {
            get {
                var playerPosition = GameObject.FindWithTag("Player").transform.position.x;
                var enemiesPositions = FindObjectsOfType<Enemy>().Select(e => (Vector2) e.transform.position).ToArray();

                return new State(enemiesPositions, playerPosition, player.Angle, player.AngularSpeed, player.UpwardSpeed);
            }
        }
    }
}