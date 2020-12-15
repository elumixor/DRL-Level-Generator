using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Common;
using Common.ByteConversions;
using RemoteComputation;
using RemoteComputation.Models;
using RL;
using UnityEngine;

public class MainController : SingletonBehaviour<MainController>
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

    public static async Task<TModel> TrainAgent<TModel>(TModel trainableModel, IEnumerable<Trajectory> episodes)
            where TModel : IRemoteModel, IByteAssignable
    {
        var asList = episodes.ToList();
        var reader = await RemoteTaskRunner.RunTask(trainableModel.Id, RemoteTask.Train, asList.MapToBytes(t => t.Bytes));
        trainableModel.AssignFromBytes(reader);
        return trainableModel;
    }

    public static Task<Trajectory> SampleTrajectory(Vector generatedData, IActor actor, IEnvironment environment)
    {
        return Task.Run(() => {
            var trajectory = new Trajectory();

            var startingState = environment.ResetEnvironment(generatedData);

            while (true) {
                var action = actor.GetAction(startingState);
                var (nextState, reward, done) = environment.Transition(startingState, action);

                trajectory.Add(startingState, action, reward, nextState);

                if (done) return trajectory;
            }
        });
    }

    public static Task<Trajectory[]> SampleTrajectories(int count,
                                                        IGenerator generator,
                                                        float difficulty,
                                                        IActor actor,
                                                        IEnvironment environment)
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

    public static async Task TrainAgentEpoch<TModel>(TModel trainableModel,
                                                     IGenerator generator,
                                                     float difficulty,
                                                     IActor actor,
                                                     IEnvironment environment,
                                                     int numTrajectories = 1,
                                                     int numEpochs = 1)
            where TModel : IRemoteModel, IByteAssignable
    {
        for (var i = 0; i < numEpochs; i++) {
            var trajectories = await SampleTrajectories(numTrajectories, generator, difficulty, actor, environment);
            await TrainAgent(trainableModel, trajectories);
        }
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
}
