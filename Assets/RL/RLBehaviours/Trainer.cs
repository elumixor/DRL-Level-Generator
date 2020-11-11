using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using NaughtyAttributes;
using RL.BackendCommunication;
using RL.Common;
using RL.Common.ByteConversions;
using RL.Configuration;
using RL.NN;
using RL.RL;
using RL.Serialization;
using UnityEditor;
using UnityEngine;
using Debug = UnityEngine.Debug;

namespace RL.RLBehaviours
{
    /// <summary>
    ///     Reads and stores global training configurations (<see cref="TrainingConfiguration"/>) Should be unique per every training setup
    /// </summary>
    public abstract class Trainer<TState, TAction, TEnvironment, TAgent, TEnvironmentInstance>
            : SingletonBehaviour<Trainer<TState, TAction, TEnvironment, TAgent, TEnvironmentInstance>>
            where TEnvironment : MonoBehaviour, IEnvironment<TState, TAction>
            where TAgent : MonoBehaviour, IAgent<TState, TAction>
            where TEnvironmentInstance : EnvironmentInstance<TState, TAction, TAgent>
    {
        const string SERVER_MAIN_PATH = "src/main.py";
        const string TCP_ADDRESS = "tcp://localhost:5555";
        const string TCP_ADDRESS_SERVER = "tcp://*:5555";

        [BoxGroup("Configuration"), SerializeField] TrainingConfiguration trainingConfiguration;

        [BoxGroup("Epochs and Episode lengths"), SerializeField] bool trainUnlimited;
        [BoxGroup("Epochs and Episode lengths"), SerializeField, MinValue(1), HideIf("trainUnlimited")] int epochs;
        [BoxGroup("Epochs and Episode lengths"), SerializeField, MinValue(1)] int episodesPerEpoch;
        [BoxGroup("Epochs and Episode lengths"), SerializeField, MinValue(1)] int maximumEpisodeLength;

        [BoxGroup("Training speed"), SerializeField, Range(0, 50)] float speed;

        [SerializeField] protected InstanceSpawner instanceSpawner;
        protected List<TEnvironmentInstance> environmentInstances;

        // On every Update() adds `speed` to itself and performs trainer steps for the number of time, rounded down to the closes integer
        float elapsed;

        // Flag if Update() should run
        bool isTraining;
        // Python backend process
        Process serverProcess;

        // Controls the general RL logic
        Trainer<TState, TAction> trainer;

        static TrainingConfiguration TrainingConfiguration => instance.trainingConfiguration;

        /// <inheritdoc/>
        protected override void Awake()
        {
            base.Awake();

            environmentInstances = instanceSpawner.Spawn<TEnvironmentInstance>().ToList();
        }

        /// <summary> The main entry point for each Training Setup </summary>
        /// 
        /// Initializes NNs in all the agents in the scene
        /// Initializes serializers, given the state size and action size
        /// Sends initial data via communicator to initialize backend
        protected virtual void Start()
        {
            // Launch backend server (use separate window to monitor stuff)
            var arguments = new Dictionary<string, string> {{"address", TCP_ADDRESS_SERVER}};
            serverProcess = ProcessRunner.CreateProcess(SERVER_MAIN_PATH, arguments, separateWindow: true);
            serverProcess.Start();

            try {
                // Open connection and ping back end to see if it is responsive
                Communicator.OpenConnection(TCP_ADDRESS);
                Communicator.Send(RequestType.WakeUp, timeout: -1);

                // If everything is ok, send initial configuration data
                var stateSize = StructuralAttribute.GetSize(typeof(TState));

                var configuration = TrainingConfiguration;
                configuration.stateSize = stateSize;

                // Communicator should return the initial nn learnable parameters
                var (nnData, startIndex) = Communicator.Send(RequestType.SendConfiguration, configuration.ToBytes(), 5000);
                var stateDict = nnData.Get<StateDict>(startIndex).result;

                Debug.Log($"Received initial state dict: {stateDict}");

                // Initialize agents with current parameters and configuration
                var actorNN = TrainingConfiguration.AlgorithmConfiguration.ConstructActorNN(stateSize, configuration.actionSize);

                foreach (var nnAgent in environmentInstances.Select(i => i.Agent).OfType<INNAgent>()) {
                    nnAgent.InitializeNN(actorNN);
                    nnAgent.SetParameters(stateDict);
                }

                // Create trainer and start training
                trainer = new Trainer<TState, TAction>(environmentInstances.Select(ti => ti.GetTrainingInstance()).ToList(),
                                                       maximumEpisodeLength,
                                                       episodesPerEpoch,
                                                       trainUnlimited ? -1 : epochs);
                trainer.Finished += () => {
                    Debug.Log("Training finished!");
                    EditorApplication.isPlaying = false;
                };

                trainer.EpochTrainingDataCollected += Train;

                isTraining = true;
                trainer.StartTraining();
            } catch (CommunicationException e) {
                Debug.LogException(e);
                EditorApplication.isPlaying = false;
            }
        }

        // Updates trainer given the speed
        void Update()
        {
            if (!isTraining) return;

            elapsed += speed;

            while (elapsed >= 1f) {
                trainer.Step();
                elapsed -= 1f;
            }
        }

        // Shuts down server and process when exiting
        void OnDestroy()
        {
            try { Communicator.Send(RequestType.ShutDown); } catch (Exception exception) { Debug.LogWarning(exception); }

            Communicator.CloseConnection();
            serverProcess.Close();
        }

        protected virtual void Train(List<List<(TState state, TAction action, float reward, TState nextState)>> epoch)
        {
            var trainingData = epoch.MapToBytes(episode => episode.MapToBytes(t => TransitionToBytes(t)));
            var (data, startIndex) = Communicator.Send(RequestType.SendTrainingData, trainingData, 10000);
            var (stateDict, _)     = data.Get<StateDict>(startIndex);

            foreach (var environmentInstance in environmentInstances)
                if (environmentInstance.Agent is INNAgent nnAgent)
                    nnAgent.SetParameters(stateDict);
        }

        protected abstract IEnumerable<byte> TransitionToBytes((TState state, TAction action, float reward, TState nextState) transition);
    }
}
