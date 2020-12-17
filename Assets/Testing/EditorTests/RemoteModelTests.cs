using System.Threading.Tasks;
using Common;
using Common.ByteConversions;
using NUnit.Framework;
using RemoteComputation;
using RemoteComputation.Models;
using RL;
using UnityEngine;

namespace Testing.EditorTests
{
    public class RemoteModelTests
    {
        class DQN : LocalInferenceNN
        {
            /// <inheritdoc/>
            public override ModelType ModelType { get; } = ModelType.DQN;

            /// <inheritdoc/>
            public override string ToString() => "DQN:\n" + nn;
        }

        [TearDown] public void TearDown() { Communicator.Close(); }

        [Test]
        public void ObtainModelWorks()
        {
            Task.Run(async () => {
                     var inputSize = 5;
                     var outputSize = 7;

                     var model = await MainController.ObtainModel<DQN>(inputSize.ToBytes(), outputSize.ToBytes());
                     Assert.AreEqual(model.ModelType, ModelType.DQN);
                     Debug.Log(model);
                 })
                .Wait(5000);
        }

        [Test]
        public void RunTaskShouldWork()
        {
            Task.Run(async () => {
                     var inputSize = 2;
                     var outputSize = 2;

                     var model = await MainController.ObtainModel<DQN>(inputSize.ToBytes(), outputSize.ToBytes());

                     Debug.Log(model);

                     var trajectory = new Trajectory();

                     var s0 = new Vector(1, 2);
                     var s1 = new Vector(2, 2);
                     var sT = new Vector(3, 2);
                     var a0 = new Vector(1);
                     var a1 = new Vector(1);
                     var r1 = 1;
                     var r2 = 1;

                     trajectory.Add(s0, a0, r2, s1);
                     trajectory.Add(s1, a1, r1, sT);

                     var difficultyEstimate = await MainController.EstimateDifficulty(model, trajectory);

                     Debug.Log($"Estimated difficulty: {difficultyEstimate}");
                 })
                .Wait(5000);
        }
    }
}
