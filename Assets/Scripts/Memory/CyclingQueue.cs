using System;
using System.Collections;
using System.Collections.Generic;

namespace Memory {
    public class CyclingQueue<T> : IEnumerable<T> {
        readonly T[] items;
        readonly int size;

        int pointer;

        public CyclingQueue(int size) {
            this.size = size;
            items = new T[size];
        }

        public bool IsFull => pointer >= size;

        public int Length => Math.Min(pointer, size);

        public T this[int i] {
            get => items[i];
            set => items[i] = value;
        }

        public IEnumerator<T> GetEnumerator() {
            var l = Length;
            for (var i = 0; i < l; i++)
                yield return items[i];
        }

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        public void Push(T item) => items[pointer++ % size] = item;

        public void Clear() => pointer = 0;
    }
}