using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using BackendCommunication;
using Common;
using Common.ByteConversions;
using Configuration;
using NaughtyAttributes;
using NN;
using RL;
using Serialization;
using UnityEditor;
using UnityEngine;
using Debug = UnityEngine.Debug;

namespace RLBehaviours
{
    /// <summary>
    ///     Reads and stores global training configurations (<see cref="TrainingSetupConfiguration"/>) Should be unique per every training setup
    /// </summary>
    public class MainController<TState, TAction, TEnvironment, TAgent, TEnvironmentInstance>
            : SingletonBehaviour<MainController<TState, TAction, TEnvironment, TAgent, TEnvironmentInstance>>
            where TEnvironment : MonoBehaviour, IEnvironment<TState, TAction>
            where TAgent : MonoBehaviour, IAgent<TState, TAction>
            where TEnvironmentInstance : EnvironmentInstance<TState, TAction, TAgent>
    {
        const string SERVER_MAIN_PATH = "src/main.py";
        const string TCP_ADDRESS = "tcp://localhost:5555";
        const string TCP_ADDRESS_SERVER = "tcp://*:5555";

        [BoxGroup("Configuration"), SerializeField] TrainingSetupConfiguration trainingSetupConfiguration;

        [BoxGroup("Epochs and Episode lengths"), SerializeField] bool trainUnlimited;
        [BoxGroup("Epochs and Episode lengths"), SerializeField, MinValue(1), HideIf("trainUnlimited")] int epochs;
        [BoxGroup("Epochs and Episode lengths"), SerializeField, MinValue(1)] int episodesPerEpoch;
        [BoxGroup("Epochs and Episode lengths"), SerializeField, MinValue(1)] int maximumEpisodeLength;

        [BoxGroup("Training speed"), SerializeField, Range(0, 500)] float speed;

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

        static TrainingSetupConfiguration TrainingSetupConfiguration => instance.trainingSetupConfiguration;

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
                var actionSize = StructuralAttribute.GetSize(typeof(TAction));
                var stateSize = StructuralAttribute.GetSize(typeof(TState));

                var configuration = TrainingSetupConfiguration;
                configuration.actionSize = actionSize;
                configuration.stateSize  = stateSize;

                // Communicator should return the initial nn learnable parameters
                var (nnData, startIndex) = Communicator.Send(RequestType.SendConfiguration, configuration.ToBytes(), 5000);
                var stateDict = nnData.Get<StateDict>(startIndex).result;

                Debug.Log($"Received state dict: {stateDict}");

                // Initialize agents with current parameters and configuration
                foreach (var nnAgent in environmentInstances.Select(i => i.Agent).OfType<INNAgent>()) {
                    nnAgent.ConstructNN(TrainingSetupConfiguration.AlgorithmConfiguration.ActorLayout);
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

        protected virtual void Train(List<List<(TState state, TAction action, float reward, TState nextState)>> epoch) { }
    }
}
