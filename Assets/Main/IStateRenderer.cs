using Common;

public interface IStateRenderer<in TState>
        where TState : Vector
{
    void RenderState(TState state);
}

public interface IStateRenderer : IStateRenderer<Vector> { }
