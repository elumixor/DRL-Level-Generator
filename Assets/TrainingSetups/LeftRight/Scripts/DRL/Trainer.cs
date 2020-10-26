using DRL.Behaviours;
using UnityEngine;

namespace TrainingSetups.LeftRight.Scripts.DRL {
    public class Trainer : Trainer<Action, State, Environment, Agent> {
        [SerializeField] float bigRewardValue;
        [SerializeField] float smallRewardValue;

        [SerializeField] float bigRewardPosition;
        [SerializeField] float smallRewardPosition;

        [SerializeField] float timeStepReward;

        void Awake() {
            environment.bigRewardValue = bigRewardValue;
            environment.smallRewardValue = smallRewardValue;
            environment.bigRewardPosition = bigRewardPosition;
            environment.smallRewardPosition = smallRewardPosition;
            environment.timeStepReward = timeStepReward;

            agent.bigRewardPosition = bigRewardPosition;
            agent.smallRewardPosition = smallRewardPosition;
        }

        void OnDrawGizmos() {
            Gizmos.color = new Color(0.35f, 0.64f, 1f);

            Gizmos.DrawCube(Vector3.left * bigRewardPosition + Vector3.up * bigRewardValue / 2, new Vector3(1, bigRewardValue, .25f));
            Gizmos.DrawCube(Vector3.right * smallRewardPosition + Vector3.up * smallRewardValue / 2,
                            new Vector3(1, smallRewardValue, .25f));
        }
    }
}