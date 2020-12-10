using System.Collections.Generic;

namespace RL
{
    public interface IState
    {
        IEnumerable<float> ToVector();
    }
}
