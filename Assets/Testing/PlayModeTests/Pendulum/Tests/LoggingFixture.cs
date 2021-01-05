using Testing.PlayModeTests.Pendulum.Generators;
using Testing.PlayModeTests.Pendulum.StateRenderers;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public class LoggingFixture : PendulumFixture<AdaptiveGenerator, StateRenderer>
    {
        // [UnityTest]
        // public IEnumerator DummyLogging()
        // {
        //     var t = Task.Run(async () => {
        //         var model = await MainController.ObtainModel<DQNPendulumModel>(5.ToBytes(), 7.ToBytes());
        //         var logOptions = new LogOptions((LogOptionName.TrajectoryReward, new LogOption(10, 100, runningAverageSmoothing: 0.8f)));
        //         await MainController.SetLogOptions(model, logOptions);
        //         Debug.Log("Yay");
        //     });
        //
        //     yield return new WaitForSeconds(10);
        //
        //     if (!t.IsCompleted) Assert.Fail("Nay");
        // }
        //
        // [UnityTest]
        // public IEnumerator TrainingLoggingWorks()
        // {
        //     yield return null;  // skip frame to allow the scene be loaded (in setup)
        //
        //     var generator = new Generator(new UniformValueInt(2, 3),
        //                                   new UniformValue(0.5f, 0.5f),
        //                                   new UniformValue(-1, 1),
        //                                   new UniformValue(1f, 2f));
        //
        //     var generatedData = generator.Generate(0);
        //
        //     // Setup stuff
        //     var state = stateRenderer.ResetEnvironment(generatedData);
        //     stateRenderer.RenderState(state);
        //
        //     Debug.Log("Set Up Done");
        //     yield return null;
        //
        //     // Start training
        //
        //     var t = Task.Run(async () => {
        //         var dqn = await MainController.ObtainModel<DQNPendulumModel>(State.SIZE.ToBytes(), Action.SIZE.ToBytes());
        //         var logOptions = new LogOptions((LogOptionName.TrajectoryReward, new LogOption(10, 100, runningAverageSmoothing: 0.8f)));
        //         await Communicator.Send(Message.SetLogOptions(dqn.Id, logOptions));
        //
        //         for (var i = 0; i < 300; i++) {
        //             Debug.Log(i);
        //             var trajectory = await MainController.SampleTrajectory(generator.Generate(0.5f), dqn, stateRenderer);
        //             await MainController.TrainAgent(dqn, new[] {trajectory});
        //         }
        //     });
        //
        //     yield return new WaitUntil(() => t.IsCompleted);
        //
        //     Debug.Log("done");
        // }
    }
}
