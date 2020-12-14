using System;
using System.IO;
using System.Runtime.InteropServices;
using Common;
using NN;
using NUnit.Framework;
using UnityEngine;

namespace Testing.EditorTests
{
    public class LayoutSerializationTests
    {
        [Test]
        public void LayoutSerializationWorks()
        {
            var bytes = File.ReadAllBytes("C:/dev/DRL-Level-Generator/Assets/Testing/EditorTests/layout.b");

            var reader = new ByteReader(bytes);
            var sequential = reader.Read<Sequential>();

            Debug.Log(sequential);
        }
    }
}
