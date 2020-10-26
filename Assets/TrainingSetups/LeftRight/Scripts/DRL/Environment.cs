using DRL.Behaviours;
using UnityEngine;

namespace TrainingSetups.LeftRight.Scripts.DRL {
    public class Environment : Environment<Action, State> {
        public float bigRewardValue;
        public float smallRewardValue;
        public float bigRewardPosition;
        public float smallRewardPosition;
        public float timeStepReward;

        [SerializeField] Transform agent;
        protected State CurrentState => new State(agent.position.x);

        public override State ResetEnvironment() {
            var x = Random.Range(-bigRewardPosition, smallRewardPosition);
            agent.transform.position = x * Vector3.right;
            return new State(x);
        }

        public override (State newState, float reward, bool isDone) Step(Action action) {
            var t = agent.transform;
            var p = t.position;
            p += (action.X * 2 - 1) * Vector3.right;
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