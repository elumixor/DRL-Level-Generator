using System;
using System.Collections.Generic;

namespace RL.RL
{
    public class Trainer<TState, TAction>
    {
        public event Action Finished = delegate { };
        public event Action<List<List<(TState state, TAction action, float reward, TState nextState)>>> EpochTrainingDataCollected = delegate { };

        readonly int episodesInEpoch;
        readonly int epochs;
        readonly List<EnvironmentInstance<TState, TAction>> trainingInstances;

        List<List<(TState state, TAction action, float reward, TState nextState)>> epochTrainingData;

        int epochIndex;

        public Trainer(List<EnvironmentInstance<TState, TAction>> trainingInstances, int maxEpisodeLength, int episodesInEpoch, int epochs = 0)
        {
            this.trainingInstances = trainingInstances;
            this.epochs            = epochs;
            this.episodesInEpoch   = episodesInEpoch;

            foreach (var trainingInstance in trainingInstances) trainingInstance.maximumEpisodeLength = maxEpisodeLength;
        }

        /// <summary>
        ///     Initializes te first epoch's samples buffer and wakes up all the training instances
        /// </summary>
        public void StartTraining()
        {
            epochTrainingData = new List<List<(TState state, TAction action, float reward, TState nextState)>>();

            foreach (var trainingInstance in trainingInstances) trainingInstance.StartNewEpisode();
        }

        // Delegates a training step to all training instances
        public void Step()
        {
            foreach (var trainingInstance in trainingInstances) {
                // Debug.Log(trainingInstance.IsDone);
                // First, check if we can collect a finished episode
                if (!trainingInstance.IsDone) { // not ready yet, so just step and continue to the next instance
                    trainingInstance.Step();
                    continue;
                }

                // We have a finished episode to collect. Add it to our training data
                var episode = trainingInstance.Episode;
                epochTrainingData.Add(episode);

                // Debug.Log(epochTrainingData.Count >= episodesInEpoch);
                if (epochTrainingData.Count >= episodesInEpoch) { // We have enough data to train, finish the current epoch
                    OnEpochFinished();
                    return;
                }

                trainingInstance.StartNewEpisode();
            }
        }

        void OnEpochFinished()
        {
            // Emit an event with collected training data.
            // It will be a responsibility of the handler to implement correct training
            EpochTrainingDataCollected(epochTrainingData);

            epochIndex++;

            if (epochs > 0 && epochIndex >= epochs) {
                Finished();
                return;
            }

            // After the training is complete, start new episodes for all the instances
            foreach (var trainingInstance in trainingInstances) trainingInstance.StartNewEpisode();

            // Also it's important clear the buffer to avoid using outdated samples
            epochTrainingData.Clear();
        }
    }
}
