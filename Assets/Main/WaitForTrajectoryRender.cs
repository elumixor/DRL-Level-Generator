using Common.ByteConversions;
using RL;
using UnityEngine;

public class WaitForTrajectoryRender<TState, TAction, TObservation, TGeneratedData> : CustomYieldInstruction
        where TState : ObservableState<TObservation>, IByteConvertible
        where TAction : Vector
        where TObservation : Vector
{
    readonly Trajectory<TState, TAction, TObservation> trajectory;
    readonly IStateRenderer<TState, TGeneratedData> stateRenderer;

    TState state;
    int currentIndex;

    readonly float deltaTime;
    float elapsed;

    /// <inheritdoc/>
    public WaitForTrajectoryRender
    (TGeneratedData generatedData,
     Trajectory<TState, TAction, TObservation> trajectory,
     IStateRenderer<TState, TGeneratedData> stateRenderer,
     float deltaTime = 0)
    {
        this.trajectory    = trajectory;
        this.stateRenderer = stateRenderer;
        this.deltaTime     = deltaTime;

        stateRenderer.Setup(generatedData);
        state = trajectory[0].state;
    }

    /// <inheritdoc/>
    public override bool keepWaiting {
        get {
            elapsed += Time.deltaTime;

            if (elapsed < deltaTime) return true;

            elapsed = 0f;

            stateRenderer.RenderState(state);
            currentIndex++;

            if (currentIndex == trajectory.Count) return false;

            state = trajectory[currentIndex].state;

            return true;
        }
    }
}
