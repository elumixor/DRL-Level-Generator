using RL.RL;
using UnityEngine;

namespace RL.RLBehaviours
{
    /// <summary>
    ///     We have an an Environment behaviour, which contains a child Agent behaviour. This object can thus also represent an EnvironmentInstance, by providing
    ///     itself as Environment, and its Agent child as an Agent.
    /// </summary>
    /// <remarks>
    ///     Must thus implement IEnvironment interface, as it will be responsible for stepping
    /// </remarks>
    public abstract class EnvironmentInstance<TState, TAction, TAgent> : MonoBehaviour, IEnvironment<TState, TAction>
            where TAgent : MonoBehaviour, IAgent<TState, TAction>
    {
        // Reference to a child Agent
        [SerializeField] TAgent agent;

        // Exposes agent and environment
        public TAgent Agent => agent;
        public IEnvironment<TState, TAction> Environment => this;

        // Must implement below methods to be a valid environment
        //
        // Will receive Step() commands to apply actions

        /// <inheritdoc/>
        public abstract TState ResetEnvironment();

        /// <inheritdoc/>
        public abstract (TState newState, float reward, bool isDone) Step(TAction action);

        /// <summary>
        ///     Provides a representation of an Environment instance, providing itself as Environment, and its Agent child as an Agent.
        /// </summary>
        /// <returns>
        ///     Environment instance that contains itself as an Environment, and a child as an Agent
        /// </returns>
        public EnvironmentInstance<TState, TAction> GetTrainingInstance() => new EnvironmentInstance<TState, TAction>(this, agent);
    }
}
