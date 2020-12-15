using Common;

namespace RL
{
    public interface IGenerator
    {
        Vector Generate(float difficulty, float randomSeed = 0f);
    }
}
