using System.Collections;
using Common;
using Common.ByteConversions;
using RemoteComputation.Logging;
using UnityEngine;
using UnityEngine.Assertions;
using UnityEngine.TestTools;
using LogOption = RemoteComputation.Logging.LogOption;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public class ContinuousRendering : PendulumFixture
    {
        [UnityTest]
        public IEnumerator ObtainDQNModelShouldWork()
        {
            DQNPendulumModel dqn = default;
            yield return new WaitForTask(async () =>
                                                 dqn = await MainController.ObtainModel<DQNPendulumModel>(Observation.SIZE.ToBytes(),
                                                                                                          Action.SIZE.ToBytes()));

            Assert.IsNotNull(dqn);
        }

        [UnityTest]
        public IEnumerator RenderThenTrainThenRenderAgain()
        {
            const int renders = 5;

            yield return SetLogOptions((LogOptionName.TrajectoryReward, new LogOption(10, 100, runningAverageSmoothing: 0.8f)),
                                       (LogOptionName.TrainingLoss, new LogOption(10, 100, runningAverageSmoothing: 0.8f)),
                                       (LogOptionName.Epsilon, new LogOption(10, 100, runningAverageSmoothing: 0.8f)));

            for (var i = 0; i < renders; i++) {
                // Sample trajectory
                var generatedData = generator.Generate(0.5f);
                var trajectoryTask = MainController.SampleTrajectory(generatedData, dqn, environment);
                yield return new WaitForTask(trajectoryTask);

                var trajectory = trajectoryTask.Result;
                Assert.IsNotNull(trajectory);

                Debug.Log(trajectory.Count);
                // Render random trajectory with the current data
                yield return new WaitForTrajectoryRender<State, Action, Observation, GeneratedData>(generatedData,
                                                                                                    trajectory,
                                                                                                    stateRenderer,
                                                                                                    .1f);

                // Train the agent
                var i1 = i;
                yield return new WaitForTask(async () => {
                    for (var j = 0; j < 100; j++) {
                        var trajectories = await MainController.SampleTrajectories(100, () => generator.Generate(0.5f), dqn, environment);
                        await MainController.TrainAgent(dqn, trajectories);
                        Debug.Log($"Training: {i1 + 1}/{renders}: {j + 1}/100");
                    }
                });
            }
        }
    }
}
