using Common;

namespace RL
{
    public interface IGenerator<out TGeneratedData>
            where TGeneratedData : Vector
    {
        TGeneratedData Generate(float difficulty, float randomSeed = 0f);
    }

    public interface IGenerator : IGenerator<Vector> { }
}
