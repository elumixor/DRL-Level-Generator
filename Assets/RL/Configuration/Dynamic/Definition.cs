using System;
using System.Collections.Generic;

namespace RL.Configuration.Dynamic
{
    [Serializable]
    public class Definition
    {
        public string name;

        public Definition(string name) => this.name = name;

        public List<Module> submodules = new List<Module>();

        public static readonly Definition ReLU = new Definition(nameof(ReLU));
        public static readonly Definition Softmax = new Definition(nameof(Softmax));
        public static readonly Definition Linear = new Definition(nameof(Linear));

        public static readonly Definition[] Predefined = {ReLU, Softmax, Linear};
        public Module this[int index] => submodules[index];
        public int SubmodulesCount => submodules.Count;
    }
}
