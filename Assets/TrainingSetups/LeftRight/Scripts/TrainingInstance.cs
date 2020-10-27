using System;
using RLBehaviours;
using TrainingSetups.LeftRight.Scripts.RL;
using UnityEngine;
using Action = TrainingSetups.LeftRight.Scripts.RL.Action;
using Random = UnityEngine.Random;

namespace TrainingSetups.LeftRight.Scripts
{
    public class TrainingInstance : TrainingInstance<State, Action, Agent>
    {
        [NonSerialized] public EnvironmentDataProvider data;

        void OnDrawGizmos()

        {
            if (data == null || Agent == null) return;

            Gizmos.color = new Color(0.35f, 0.64f, 1f);

            // Rewards
            Gizmos.DrawCube(Vector3.left * data.bigRewardPosition + Vector3.up * data.bigRewardValue / 2,
                            new Vector3(1, data.bigRewardValue, .25f));
            Gizmos.DrawCube(Vector3.right * data.smallRewardPosition + Vector3.up * data.smallRewardValue / 2,
                            new Vector3(1, data.smallRewardValue, .25f));

            // position
            Gizmos.color = new Color(1f, 0.59f, 0.37f);
            Gizmos.DrawSphere(Agent.transform.position, .5f);
        }

        /// <inheritdoc/>
        public override State ResetEnvironment()
        {
            var x = Random.Range(-data.spawnLeft, data.spawnRight);
            Agent.transform.position = x * Vector3.right;
            return new State(x);
        }

        /// <inheritdoc/>
        public override (State newState, float reward, bool isDone) Step(Action action)
        {
            var movement = (action.X * 2 - 1) * data.agentStepSize;
            var t = Agent.transform;
            var position = t.position + movement * Vector3.right;
            t.position = position;
            var x = position.x;

            var reachedBig = x   <= -data.bigRewardPosition;
            var reachedSmall = x >= data.smallRewardPosition;
            var reward = reachedBig ? data.bigRewardValue : reachedSmall ? data.smallRewardValue : data.timeStepReward;
            var done = reachedBig || reachedSmall;

            return (new State(x), reward, done);
        }
    }
}
