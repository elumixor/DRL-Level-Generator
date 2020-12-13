using Common;

namespace MainScripts
{
    public interface IGenerator
    {
        Vector Generate(float difficulty, float randomSeed = 0f);
    }
}
