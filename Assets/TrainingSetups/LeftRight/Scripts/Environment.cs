using System;
using RL.RLBehaviours;
using UnityEngine;
using Random = UnityEngine.Random;

namespace TrainingSetups.LeftRight.Scripts
{
    public class Environment : EnvironmentInstance<State, int, Agent>
    {
        [NonSerialized] public EnvironmentSettings settings;

        void OnDrawGizmos()

        {
            Gizmos.matrix = transform.localToWorldMatrix;

            if (settings == null || Agent == null) return;

            // Spawn position
            Gizmos.color = new Color(0.35f, 0.5f, 0.37f);
            Gizmos.DrawCube(Vector3.right * (settings.spawnRight + settings.spawnLeft) / 2,
                            Vector3.right * (settings.spawnRight - settings.spawnLeft) + Vector3.forward);
            // Rewards
            Gizmos.color = new Color(0.35f, 0.64f, 1f);
            Gizmos.DrawCube(Vector3.right * settings.bigRewardPosition + Vector3.up * settings.bigRewardValue / 2,
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
            var x = Random.Range(settings.spawnLeft, settings.spawnRight);
            Agent.transform.position = x * Vector3.right;
            return new State(x);
        }

        /// <inheritdoc/>
        public override (State newState, float reward, bool isDone) Step(int action)
        {
            var movement = (action * 2 - 1) * settings.agentStepSize;
            var t = Agent.transform;
            var x = t.position.x + movement;
            t.position = new Vector3(x, 0, 0);

            var reachedBig = x   <= settings.bigRewardPosition;
            var reachedSmall = x >= settings.smallRewardPosition;
            var reward = reachedBig ? settings.bigRewardValue : reachedSmall ? settings.smallRewardValue : settings.timeStepReward;
            var done = reachedBig || reachedSmall;

            return (new State(x), reward, done);
        }
    }
}
