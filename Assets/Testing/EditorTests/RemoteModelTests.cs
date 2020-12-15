using System;
using Common;
using Common.ByteConversions;
using NUnit.Framework;
using RemoteComputation.Models;
using RL;

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

        [Test]
        public void RemoteModelWorks()
        {
            var inputSize = 5;
            var outputSize = 7;

            var modelTask = MainController.ObtainModel<DQN>(inputSize.ToBytes(), outputSize.ToBytes());
            modelTask.Wait();

            Console.WriteLine(modelTask.Result);
        }

        [Test]
        public void RunTaskShouldWork()
        {
            var inputSize = 2;
            var outputSize = 2;

            var modelTask = MainController.ObtainModel<DQN>(inputSize.ToBytes(), outputSize.ToBytes());
            modelTask.Wait();

            var model = modelTask.Result;

            Console.WriteLine(model);

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

            var difficultyEstimate = MainController.EstimateDifficulty(model, trajectory);

            difficultyEstimate.Wait();

            Console.WriteLine($"Estimated difficulty: {difficultyEstimate.Result}");
        }
    }
}
