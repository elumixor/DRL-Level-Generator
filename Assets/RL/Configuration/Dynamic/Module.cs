using System;

namespace RL.Configuration.Dynamic
{
    [Serializable]
    public class Module
    {
        public string definitionName;

        public bool inputSizeInferred;
        public bool outputSizeInferred;

        public int inputSizeFixed;
        public int outputSizeFixed;

        public Module(string name) => definitionName = name;
    }
}
