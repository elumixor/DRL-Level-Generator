﻿using System.Linq;
using Common;
using DRL.Behaviours;
using NaughtyAttributes;
using Player;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class InferenceEnvironment : Environment<Action, State> {
        [SerializeField, Required] PlayerBehaviouralController player;
        [SerializeField, Required] PlayerInputHandler playerInputHandler;

        bool isDone;

        // void Start() => player.Collided += () => isDone = true;
        protected override void FixedUpdate() {
            base.FixedUpdate();

            if (player.transform.position.y >= 9f) isDone = true;
        }
        public override void ResetEnvironment() {
            player.ResetState();
            isDone = false;
            foreach (var followTransform in FindObjectsOfType<FollowTransform>()) followTransform.Synchronize();
        }

        public override (float reward, bool isDone) Step(Action action) {
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