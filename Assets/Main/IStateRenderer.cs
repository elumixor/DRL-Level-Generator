using RL;

public interface IStateRenderer<in TState, in TGeneratedData>
{
    void Setup(TGeneratedData generatedData);
    void RenderState(TState state);
}

public interface IStateRenderer : IStateRenderer<Vector, Vector> { }
