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
        protected override State CurrentState => new State(agent.position.x);

        public override void ResetEnvironment() {
            agent.transform.position = Random.Range(-bigRewardPosition, smallRewardPosition) * Vector3.left;
        }

        public override (float reward, bool isDone) Step(Action action) {
            var t = agent.transform;
            var p = t.position;
            p += (action.X - 1) * 2 * Vector3.left;
            t.position = p;
            var x = p.x;


            var reachedBig = x   <= -bigRewardPosition;
            var reachedSmall = x >= smallRewardPosition;
            var reward = reachedBig ? bigRewardValue : reachedSmall ? smallRewardValue : timeStepReward;
            var done = reachedBig || reachedSmall;

            return (reward, done);
        }
    }
}