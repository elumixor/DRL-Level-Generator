using System.Collections;
using Common;
using Common.ByteConversions;
using RemoteComputation;
using RemoteComputation.Logging;
using RemoteComputation.Models;
using RL;

namespace Testing.TestCommon
{
    public static class Experiment
    {
        public static LogOptions DefaultLogOptions =>
                new LogOptions((LogOptionName.TrajectoryReward, new LogOption(10, 100, runningAverageSmoothing: 0.8f)),
                               (LogOptionName.TrainingLoss, new LogOption(10, 100, runningAverageSmoothing: 0.8f)),
                               (LogOptionName.Epsilon, new LogOption(10, 100, runningAverageSmoothing: 0.8f)));

        public static IEnumerator SetDefaultLogOptions(IRemoteModel model)
        {
            yield return new WaitForTask(async () => {
                var logOptions = new LogOptions((LogOptionName.TrajectoryReward, new LogOption(10, 100, runningAverageSmoothing: 0.8f)),
                                                (LogOptionName.TrainingLoss, new LogOption(10, 100, runningAverageSmoothing: 0.8f)),
                                                (LogOptionName.Epsilon, new LogOption(10, 100, runningAverageSmoothing: 0.8f)));
                await Communicator.Send(Message.SetLogOptions(model.Id, logOptions));
            });
        }

        public static IEnumerator SetLogOptions(IRemoteModel model, LogOptions logOptions)
        {
            yield return new WaitForTask(async () => await Communicator.Send(Message.SetLogOptions(model.Id, logOptions)));
        }

        public static IEnumerator PerformTrainingExperiment<TGeneratedData, TState, TAction, TObservation>
        (IGenerator<TGeneratedData> generator,
         IActor<TObservation, TAction> actor,
         IStateRenderer<TState, TGeneratedData> stateRenderer,
         IEnvironment<TGeneratedData, TState, TAction> environment,
         ITrainableRemoteModel trainableRemoteModel,
         int epochs,
         int trainingsInEpoch,
         int trajectoriesForTraining,
         int rendersInEpoch,
         float difficulty,
         float deltaTime) where TState : ObservableState<TObservation>, IByteConvertible
                          where TObservation : Vector
                          where TAction : Vector
                          where TGeneratedData : Vector
        {
            for (var epoch = 0; epoch < epochs; epoch++) {
                // Render several trajectories
                for (var render = 0; render < rendersInEpoch; render++)
                    yield return Render(generator, actor, stateRenderer, environment, difficulty, deltaTime: deltaTime);

                // Perform training
                for (var training = 0; training < trainingsInEpoch; training++)
                    yield return Train(generator, actor, environment, trainableRemoteModel, difficulty, trajectoriesForTraining);
            }
        }

        public static IEnumerator Render<TGeneratedData, TState, TAction, TObservation>
        (IGenerator<TGeneratedData> generator,
         IActor<TObservation, TAction> actor,
         IStateRenderer<TState, TGeneratedData> stateRenderer,
         IEnvironment<TGeneratedData, TState, TAction> environment,
         float difficulty,
         float randomSeed = 0f,
         float deltaTime = 0.1f) where TState : ObservableState<TObservation>, IByteConvertible
                                 where TObservation : Vector
                                 where TAction : Vector
                                 where TGeneratedData : Vector
        {
            var genData = generator.Generate(difficulty, randomSeed);

            var trajectoryTask = MainController.SampleTrajectory(genData, actor, environment);
            yield return new WaitForTask(trajectoryTask);

            var trajectory = trajectoryTask.Result;
            yield return new WaitForTrajectoryRender<TState, TAction, TObservation, TGeneratedData>(genData,
                                                                                                    trajectory,
                                                                                                    stateRenderer,
                                                                                                    deltaTime);
        }

        public static IEnumerator Train<TGeneratedData, TState, TAction, TObservation>
        (IGenerator<TGeneratedData> generator,
         IActor<TObservation, TAction> actor,
         IEnvironment<TGeneratedData, TState, TAction> environment,
         ITrainableRemoteModel remoteModel,
         float difficulty,
         int trajectoriesForTraining,
         float randomSeed = 0f) where TState : ObservableState<TObservation>, IByteConvertible
                                where TObservation : Vector
                                where TAction : Vector
                                where TGeneratedData : Vector
        {
            yield return new WaitForTask(async () => {
                var trajectories = await MainController.SampleTrajectories(trajectoriesForTraining,
                                                                           generator,
                                                                           difficulty,
                                                                           actor,
                                                                           environment,
                                                                           randomSeed);
                await MainController.TrainAgent(remoteModel, trajectories);
            });
        }

        public static IEnumerator ShowLog(IRemoteModel remoteModel)
        {
            yield return new WaitForTask(async () => { await Communicator.Send(Message.ShowLog(remoteModel.Id)); });
        }
    }
}
