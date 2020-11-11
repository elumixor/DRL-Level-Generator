using System;
using System.Collections.Generic;
using System.ComponentModel;

namespace RL.Common
{
    [Serializable]
    public class EnumDictionary<TEnum, TValue>
            where TEnum : Enum
    {
        public TValue[] data;
        public TEnum[] values;

        public EnumDictionary()
        {
            values = (TEnum[]) Enum.GetValues(typeof(TEnum));
            var length = values.Length;
            data = new TValue[length];
            FillDefaults();
        }

        public EnumDictionary(IEnumerable<(TEnum @enum, TValue value)> valuePairs) : this()
        {
            foreach (var (@enum, value) in valuePairs) this[@enum] = value;
        }

        public TValue this[TEnum i] {
            get => data[getIndex(i)];
            set => data[getIndex(i)] = value;
        }

        public TValue this[int i] {
            get => data[i];
            set => data[i] = value;
        }

        public void Clear() { FillDefaults(); }

        void FillDefaults()
        {
            for (var i = 0; i < data.Length; i++) data[i] = default;
        }

        int getIndex(TEnum i)
        {
            for (var j = 0; j < values.Length; j++)
                if (Equals(values[j], i))
                    return j;

            throw new InvalidEnumArgumentException();
        }
    }
}
