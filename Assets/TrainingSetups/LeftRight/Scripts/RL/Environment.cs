using System;
using RL.Behaviours;
using UnityEngine;
using Random = UnityEngine.Random;

namespace TrainingSetups.LeftRight.Scripts.RL {
    public class Environment : Environment<Action, State> {
        [SerializeField] Transform agent;
        [NonSerialized] public float bigRewardPosition;
        [NonSerialized] public float bigRewardValue;
        [NonSerialized] public float movementDistance;
        [NonSerialized] public float smallRewardPosition;
        [NonSerialized] public float smallRewardValue;
        [NonSerialized] public float spawnLeft;
        [NonSerialized] public float spawnRight;
        [NonSerialized] public float timeStepReward;
        protected State CurrentState => new State(agent.position.x);

        public override State ResetEnvironment() {
            var x = Random.Range(-spawnLeft, spawnRight);
            agent.transform.position = x * Vector3.right;
            return new State(x);
        }

        public override (State newState, float reward, bool isDone) Step(Action action) {
            var t = agent.transform;
            var p = t.position;
            p += (action.X * 2 - 1) * movementDistance * Vector3.right;
            t.position = p;
            var x = p.x;


            var reachedBig = x   <= -bigRewardPosition;
            var reachedSmall = x >= smallRewardPosition;
            var reward = reachedBig ? bigRewardValue : reachedSmall ? smallRewardValue : timeStepReward;
            var done = reachedBig || reachedSmall;

            return (CurrentState, reward, done);
        }
    }
}