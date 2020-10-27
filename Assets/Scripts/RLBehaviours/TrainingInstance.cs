using RL;
using UnityEngine;

namespace RLBehaviours
{
    public abstract class TrainingInstance<TState, TAction, TAgent> : MonoBehaviour, IEnvironment<TState, TAction>
            where TAgent : MonoBehaviour, IAgent<TState, TAction>
    {
        [SerializeField] TAgent agent;
        public TAgent Agent => agent;

        /// <inheritdoc/>
        public abstract TState ResetEnvironment();

        /// <inheritdoc/>
        public abstract (TState newState, float reward, bool isDone) Step(TAction action);

        public TrainingInstance<TState, TAction> GetTrainingInstance() => new TrainingInstance<TState, TAction>(this, agent);
    }
}
