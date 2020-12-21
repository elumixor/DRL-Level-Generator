using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Common;
using Common.ByteConversions;
using JetBrains.Annotations;
using RemoteComputation;
using RemoteComputation.Logging;
using RemoteComputation.Models;
using RL;
using UnityEngine;

public static class MainController
{
    /* High-level abstract stuff */

    public static async Task<T> ObtainModel<T>()
            where T : IByteAssignable, IRemoteModel, new()
    {
        var result = new T();
        var reader = await Communicator.Send(Message.ObtainModel(result.ModelType));
        result.AssignFromBytes(reader);
        return result;
    }

    public static async Task<T> ObtainModel<T>(params IEnumerable<byte>[] args)
            where T : IByteAssignable, IRemoteModel, new()
    {
        var result = new T();
        var reader = await Communicator.Send(Message.ObtainModel(result.ModelType, args));
        result.AssignFromBytes(reader);
        return result;
    }

    public static async Task<T> LoadModel<T>(string path)
            where T : IByteAssignable, IRemoteModel, new()
    {
        var result = new T();
        var reader = await Communicator.Send(Message.LoadModel(path));
        result.AssignFromBytes(reader);
        return result;
    }

    public static async Task SaveModel(IRemoteModel model, string path) { await Communicator.Send(Message.SaveModel(model.Id, path)); }

    /* More specific stuff */

    public static async Task TrainAgent<TModel>(TModel trainableModel, IReadOnlyCollection<Trajectory> trajectories)
            where TModel : IRemoteModel, IByteAssignable
    {
        var reader = await RemoteTaskRunner.RunTask(trainableModel.Id, RemoteTask.Train, trajectories.MapToBytes(t => t.Bytes));
        trainableModel.AssignFromBytes(reader);
    }

    public static Task<Trajectory> SampleTrajectory<TGenData, TState, TAction>(TGenData generatedData,
                                                                               IActor<TState, TAction> actor,
                                                                               IEnvironment<TGenData, TState, TAction> environment)
            where TGenData : Vector
            where TState : Vector
            where TAction : Vector
    {
        return Task.Run(() => {
            var trajectory = new Trajectory();

            var startingState = environment.ResetEnvironment(generatedData);

            while (true) {
                var action = actor.GetAction(startingState);
                var (nextState, reward, done) = environment.Transition(startingState, action);

                trajectory.Add(startingState, action, reward, nextState);

                if (done) return trajectory;

                startingState = nextState;
            }
        });
    }

    public static Task<Trajectory> SampleTrajectory(Vector generatedData,
                                                    IActor actor,
                                                    IEnvironment environment,
                                                    IStateRenderer stateRenderer,
                                                    int renderEvery = 1)
    {
        return Task.Run(() => {
            var trajectory = new Trajectory();

            var startingState = environment.ResetEnvironment(generatedData);

            var currentRendered = 1;

            while (true) {
                if (currentRendered >= renderEvery) {
                    currentRendered = 0;
                    stateRenderer.RenderState(startingState);
                }

                var action = actor.GetAction(startingState);
                var (nextState, reward, done) = environment.Transition(startingState, action);

                trajectory.Add(startingState, action, reward, nextState);

                if (done) return trajectory;

                currentRendered++;
                startingState = nextState;
            }
        });
    }

    public static Task<Trajectory[]> SampleTrajectories<TGenData, TState, TAction>(int count,
                                                                                   IGenerator<TGenData> generator,
                                                                                   float difficulty,
                                                                                   IActor<TState, TAction> actor,
                                                                                   IEnvironment<TGenData, TState, TAction> environment)
            where TGenData : Vector
            where TState : Vector
            where TAction : Vector
    {
        // todo: maybe this is better to do with multiple task and mutex synchronization
        return Task.Run(() => {
            var result = new Trajectory[count];

            for (var i = 0; i < count; i++) {
                var seed = Random.value;
                var generatedData = generator.Generate(difficulty, seed);
                var sampleTask = SampleTrajectory(generatedData, actor, environment);
                sampleTask.Wait();
                result[i] = sampleTask.Result;
            }

            return result;
        });
    }

    public static async Task TrainAgent<TModel, TGenData, TState, TAction>(TModel trainableModel,
                                                                           IGenerator<TGenData> generator,
                                                                           float difficulty,
                                                                           IActor<TState, TAction> actor,
                                                                           IEnvironment<TGenData, TState, TAction> environment,
                                                                           int numTrajectories = 1,
                                                                           int numEpochs = 1,
                                                                           LogOptions logOptions = null)
            where TModel : IRemoteModel, IByteAssignable
            where TGenData : Vector
            where TState : Vector
            where TAction : Vector
    {
        if (logOptions != null) await SetLogOptions(trainableModel, logOptions);

        Debug.Log($"? {numEpochs}");

        for (var i = 0; i < numEpochs; i++) {
            Debug.Log(i);
            var trajectories = await SampleTrajectories(numTrajectories, generator, difficulty, actor, environment);
            await TrainAgent(trainableModel, trajectories);
        }

        Debug.Log("Returning?????");
    }

    public static async Task<float> EstimateDifficulty(IRemoteModel estimator, Trajectory trajectory)
    {
        var reader = await RemoteTaskRunner.RunTask(estimator.Id, RemoteTask.EstimateDifficulty, trajectory.Bytes);
        return reader.ReadFloat();
    }

    public static async Task<float> EstimateDifficulty(IRemoteModel estimator, Trajectory[] trajectories)
    {
        var reader = await RemoteTaskRunner.RunTask(estimator.Id,
                                                    RemoteTask.EstimateDifficulty,
                                                    trajectories.Length.ToBytes().Concat(trajectories.SelectMany(t => t.Bytes)));

        return reader.ReadFloat();
    }

    public static async Task<float> EstimateDifficulty(IEnumerable<IRemoteModel> estimators, IEnumerable<Trajectory> trajectories)
    {
        var t = trajectories.ToArray();

        var difficulties = new List<float>();
        foreach (var estimator in estimators) difficulties.Add(await EstimateDifficulty(estimator, t));

        return difficulties.Mean();
    }

    /* Helpers */

    public static async Task SetLogOptions(IRemoteModel remoteModel, [NotNull] LogOptions logOptions)
    {
        await Communicator.Send(Message.SetLogOptions(remoteModel.Id, logOptions));
    }
}
