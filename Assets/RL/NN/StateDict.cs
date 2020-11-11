using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;
using JetBrains.Annotations;

namespace RL.NN
{
    public struct StateDict : IByteSerializable
    {
        [NotNull] public Dictionary<ModuleParameterName, Tensor> selfParameters;
        [NotNull] public List<(int[] path, (ModuleParameterName name, Tensor value) parameter)> childParameters;

        public StateDict([NotNull] Dictionary<ModuleParameterName, Tensor> selfParameters,
                         [NotNull] List<(int[] path, (ModuleParameterName name, Tensor value) parameter)> childParameters)
        {
            this.selfParameters  = selfParameters;
            this.childParameters = childParameters;
        }

        public StateDict(Dictionary<ModuleParameterName, Tensor> selfParameters)
        {
            this.selfParameters = selfParameters;
            childParameters     = new List<(int[] path, (ModuleParameterName name, Tensor value) parameter)>();
        }

        public StateDict(List<(int[] path, (ModuleParameterName name, Tensor value) parameter)> childParameters)
        {
            selfParameters       = new Dictionary<ModuleParameterName, Tensor>();
            this.childParameters = childParameters;
        }

        public int Length => (int) selfParameters?.Count + (childParameters?.Count ?? 0);

        public IEnumerable<byte> ToBytes()
        {
            var countBytes = Length.ToBytes();
            var selfBytes = selfParameters.SelectMany(kvp => kvp.Key.ToString().ToBytes().Concat(kvp.Value.ToBytes()));
            var childBytes = childParameters.SelectMany(arg => {
                var (path, (name, value)) = arg;
                return (string.Join(".", path) + (path.Length > 0 ? "." : "") + name).ToBytes().Concat(value.ToBytes());
            });

            return countBytes.ConcatMany(selfBytes, childBytes);
        }

        public int AssignFromBytes(byte[] bytes, int startIndex = 0)
        {
            var numParameters = bytes.ToInt(startIndex);
            var bytesReadTotal = sizeof(int);

            selfParameters  = new Dictionary<ModuleParameterName, Tensor>();
            childParameters = new List<(int[] path, (ModuleParameterName name, Tensor value) parameter)>();

            for (var i = 0; i < numParameters; i++) {
                var (parameterNameString, bytesReadKey) =  bytes.GetString(startIndex + bytesReadTotal);
                bytesReadTotal                          += bytesReadKey;

                var (parameterValue, bytesReadValue) =  bytes.Get<Tensor>(startIndex + bytesReadTotal);
                bytesReadTotal                       += bytesReadValue;

                var split = parameterNameString.Split('.');
                var parameterName = (ModuleParameterName) Enum.Parse(typeof(ModuleParameterName), split[split.Length - 1]);

                if (split.Length < 2) {
                    selfParameters[parameterName] = parameterValue;
                    continue;
                }

                var path = new int[split.Length - 1];
                for (var j = 0; j < split.Length - 1; j++) path[j] = int.Parse(split[j]);

                childParameters.Add((path, (parameterName, parameterValue)));
            }

            return bytesReadTotal;
        }

        public override string ToString()
        {
            var header = $"StateDict with {Length} parameters:\n";

            var selfBytes = selfParameters.Count > 0 ? selfParameters.Select(kvp => kvp.Key + ":\n" + kvp.Value).Aggregate((a, b) => a + "\n" + b) + "\n" : "";
            var childBytes = childParameters.Count > 0
                                     ? childParameters.Select(arg => {
                                                           var (path, (name, value)) = arg;
                                                           return string.Join(".", path) + (path.Length > 0 ? "." : "") + name + "\n" + value;
                                                       })
                                                      .Aggregate((a, b) => a + "\n" + b) + "\n"
                                     : "";

            return header + selfBytes + childBytes;
        }

        bool Equals(StateDict other)
        {
            if (!selfParameters.SequenceEqual(other.selfParameters)) return false;
            if (childParameters.Count != other.childParameters.Count) return false;

            for (var i = 0; i < childParameters.Count; i++) {
                var (p1, (n1, t1)) = childParameters[i];
                var (p2, (n2, t2)) = other.childParameters[i];

                if (!p1.SequenceEqual(p2) || !Equals(n1, n2) || !Equals(t1, t2)) return false;
            }

            return true;
        }

        public override bool Equals(object obj) => obj is StateDict other && Equals(other);

        public override int GetHashCode() => throw new NotImplementedException();
    }
}
