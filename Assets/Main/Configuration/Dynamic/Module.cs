using System;

namespace Configuration.Dynamic
{
    [Serializable]
    public class Module
    {
        public string definitionName;

        public bool inputSizeInferred;
        public int inputSizeFixed;

        public int outputSizeFixed;
        public bool outputSizeInferred;

        public bool HasFixedInput => !inputSizeInferred;
        public bool HasFixedOutput => !outputSizeInferred;

        public Module(string name) => definitionName = name;
    }
}
