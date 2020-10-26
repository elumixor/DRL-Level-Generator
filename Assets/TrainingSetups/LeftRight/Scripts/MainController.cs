using NaughtyAttributes;
using TrainingSetups.LeftRight.Scripts.RL;
using UnityEngine;

namespace TrainingSetups.LeftRight.Scripts {
    public class MainController : MainController<Action, State, Environment, Agent> {
        [BoxGroup("Reward Value"), SerializeField] float bigRewardValue;
        [BoxGroup("Reward Value"), SerializeField] float smallRewardValue;
        [BoxGroup("Reward Value"), SerializeField] float timeStepReward;

        [BoxGroup("Reward Position"), SerializeField] float bigRewardPosition;
        [BoxGroup("Reward Position"), SerializeField] float smallRewardPosition;

        [BoxGroup("Spawn"), SerializeField] float spawnLeft;
        [BoxGroup("Spawn"), SerializeField] float spawnRight;

        [BoxGroup("Movement"), SerializeField, Range(1e-7f, 5f)] float agentMovementDistance;

        protected override void Awake() {
            base.Awake();

            environment.bigRewardValue = bigRewardValue;
            environment.smallRewardValue = smallRewardValue;
            environment.bigRewardPosition = bigRewardPosition;
            environment.smallRewardPosition = smallRewardPosition;
            environment.spawnLeft = spawnLeft;
            environment.spawnRight = spawnRight;
            environment.timeStepReward = timeStepReward;
            environment.movementDistance = agentMovementDistance;
        }

        void OnDrawGizmos() {
            Gizmos.color = new Color(0.35f, 0.64f, 1f);

            // Rewards
            Gizmos.DrawCube(Vector3.left * bigRewardPosition + Vector3.up * bigRewardValue / 2, new Vector3(1, bigRewardValue, .25f));
            Gizmos.DrawCube(Vector3.right * smallRewardPosition + Vector3.up * smallRewardValue / 2,
                            new Vector3(1, smallRewardValue, .25f));

            // position
            Gizmos.color = new Color(1f, 0.59f, 0.37f);
            Gizmos.DrawSphere(agent.transform.position, .5f);
        }
    }
}