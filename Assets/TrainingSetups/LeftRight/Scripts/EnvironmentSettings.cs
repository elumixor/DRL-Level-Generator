using NaughtyAttributes;
using UnityEngine;

namespace TrainingSetups.LeftRight.Scripts
{
    public class EnvironmentSettings : MonoBehaviour
    {
        [BoxGroup("Reward Value")] public float bigRewardValue;
        [BoxGroup("Reward Value")] public float smallRewardValue;
        [BoxGroup("Reward Value")] public float timeStepReward;

        [BoxGroup("Reward Position")] public float bigRewardPosition;
        [BoxGroup("Reward Position")] public float smallRewardPosition;

        [BoxGroup("Spawn")] public float spawnLeft;
        [BoxGroup("Spawn")] public float spawnRight;

        [BoxGroup("Movement"), Range(1e-7f, 5f)] public float agentStepSize;
    }
}
