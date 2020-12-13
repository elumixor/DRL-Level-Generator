using System.Collections.Generic;
using Common;

namespace RL
{
    public interface IActor
    {
        Vector GetAction(Vector state);
    }
}
