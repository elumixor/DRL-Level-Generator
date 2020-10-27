using System;
using RLBehaviours;
using UnityEngine;
using Random = UnityEngine.Random;

namespace TrainingSetups.LeftRight.Scripts
{
    public class EnvironmentInstance : EnvironmentInstance<State, Action, Agent>
    {
        [NonSerialized] public EnvironmentSettings settings;

        void OnDrawGizmos()

        {
            if (settings == null || Agent == null) return;

            Gizmos.color = new Color(0.35f, 0.64f, 1f);

            // Rewards
            Gizmos.DrawCube(Vector3.left * settings.bigRewardPosition + Vector3.up * settings.bigRewardValue / 2,
                            new Vector3(1, settings.bigRewardValue, .25f));
            Gizmos.DrawCube(Vector3.right * settings.smallRewardPosition + Vector3.up * settings.smallRewardValue / 2,
                            new Vector3(1, settings.smallRewardValue, .25f));

            // position
            Gizmos.color = new Color(1f, 0.59f, 0.37f);
            Gizmos.DrawSphere(Agent.transform.position, .5f);
        }

        /// <inheritdoc/>
        public override State ResetEnvironment()
        {
            var x = Random.Range(-settings.spawnLeft, settings.spawnRight);
            Agent.transform.position = x * Vector3.right;
            return new State(x);
        }

        /// <inheritdoc/>
        public override (State newState, float reward, bool isDone) Step(Action action)
        {
            var movement = (action.X * 2 - 1) * settings.agentStepSize;
            var t = Agent.transform;
            var x = t.position.x + movement;
            t.position = new Vector3(x, 0, 0);

            var reachedBig = x   <= -settings.bigRewardPosition;
            var reachedSmall = x >= settings.smallRewardPosition;
            var reward = reachedBig ? settings.bigRewardValue : reachedSmall ? settings.smallRewardValue : settings.timeStepReward;
            var done = reachedBig || reachedSmall;

            var doneString = done ? "done" : "not done";

            Debug.Log($"Environment instance is: {doneString} (x={x})");
            return (new State(x), reward, done);
        }
    }
}
